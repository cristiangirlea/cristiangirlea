"""Generate repository-hosted GitHub cards from public repository data."""
import json
import os
import re
from collections import Counter
from datetime import date, datetime, timedelta, timezone
from html import escape
from pathlib import Path
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
QUERY = '''query($owner: String!, $cursor: String, $from: DateTime!, $to: DateTime!) {
  user(login: $owner) {
    repositories(first: 100, after: $cursor, privacy: PUBLIC, isFork: false,
                 ownerAffiliations: OWNER) {
      nodes { nameWithOwner isArchived stargazerCount
        languages(first: 100, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name color } } pageInfo { hasNextPage }
        }
      }
      pageInfo { hasNextPage endCursor }
    }
    contributionsCollection(from: $from, to: $to) {
      commitContributionsByRepository(maxRepositories: 100) {
        repository { isPrivate } contributions { totalCount }
      }
      contributionCalendar { totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}'''


def graphql(variables):
    headers = {'Authorization': 'Bearer ' + os.environ['GH_TOKEN'],
               'Content-Type': 'application/json', 'User-Agent': 'github-profile-cards'}
    body = json.dumps({'query': QUERY, 'variables': variables}).encode()
    with urlopen(Request('https://api.github.com/graphql', data=body, headers=headers), timeout=30) as response:
        result = json.load(response)
    if result.get('errors') or not result.get('data', {}).get('user'):
        raise ValueError('GitHub did not return a complete public profile')
    return result['data']['user']


def streaks(days, today):
    """A quiet current UTC day does not end yesterday's streak."""
    counts = {date.fromisoformat(day['date']): day['contributionCount'] for day in days}
    current = longest = run = 0
    previous = None
    for day in sorted(counts):
        if previous is not None and day != previous + timedelta(days=1):
            raise ValueError('Incomplete contribution calendar')
        run = run + 1 if counts[day] else 0
        longest = max(longest, run)
        previous = day
    cursor = today if counts.get(today) else today - timedelta(days=1)
    while counts.get(cursor):
        current += 1
        cursor -= timedelta(days=1)
    return {'current': current, 'longest': longest}


def collect(owner, now=None):
    now = now or datetime.now(timezone.utc)
    today = now.date()
    start = today - timedelta(days=364)
    variables = {'owner': owner, 'cursor': None,
                 'from': start.isoformat() + 'T00:00:00Z', 'to': now.isoformat()}
    repos = []
    while True:
        user = graphql(variables)
        page = user['repositories']
        repos.extend(r for r in page['nodes'] if not r['isArchived'])
        if not page['pageInfo']['hasNextPage']:
            break
        cursor = page['pageInfo']['endCursor']
        if not cursor or cursor == variables['cursor']:
            raise ValueError('Repository pagination did not advance')
        variables['cursor'] = cursor
    languages, colors = Counter(), {}
    for repo in repos:
        if repo['languages']['pageInfo']['hasNextPage']:
            raise ValueError('Incomplete repository language breakdown')
        for edge in repo['languages']['edges']:
            name = edge['node']['name']
            languages[name] += edge['size']
            colors[name] = edge['node']['color'] or '#64748b'
    calendar = user['contributionsCollection']['contributionCalendar']
    commit_repos = user['contributionsCollection']['commitContributionsByRepository']
    if len(commit_repos) == 100:
        raise ValueError('Public commit repository list may be truncated')
    public_commits = sum(r['contributions']['totalCount'] for r in commit_repos if not r['repository']['isPrivate'])
    days = [d for week in calendar['weeks'] for d in week['contributionDays']
            if start.isoformat() <= d['date'] <= today.isoformat()]
    if len(days) != 365 or sum(d['contributionCount'] for d in days) != calendar['totalContributions']:
        raise ValueError('Incomplete contribution calendar totals')
    upstream = json.loads((ROOT / 'data/contributions.json').read_text(encoding='utf-8'))
    if upstream['owner'] != owner:
        raise ValueError('Upstream contribution snapshot belongs to another user')
    language_rows = [{'name': name, 'bytes': size, 'color': colors[name]}
                     for name, size in languages.most_common()]
    return {'owner': owner, 'checked_at': now.strftime('%Y-%m-%d %H:%M UTC'),
            'period_start': start.isoformat(), 'period_end': today.isoformat(),
            'repository_scope': 'Public, owned, non-fork, non-archived repositories',
            'repositories': len(repos), 'stars': sum(r['stargazerCount'] for r in repos),
            'repository_names': sorted(r['nameWithOwner'] for r in repos),
            'languages': language_rows, 'calendar_contributions': calendar['totalContributions'],
            'public_commits': public_commits,
            'streaks': streaks(days, today),
            'upstream_merged': sum(r['merged'] for r in upstream['repositories']),
            'upstream_open': sum(r['open'] for r in upstream['repositories'])}


def text(x, y, value, color, size=14, weight=400, anchor='start'):
    return (f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" '
            f'font-weight="{weight}" text-anchor="{anchor}">{escape(str(value))}</text>')


def card(title, width, height, content, theme):
    palette = {'light': ('#ffffff', '#d7e3f3', '#152d51', '#445d7e', '#245bcc'),
               'dark': ('#14233e', '#385e8c', '#edf4ff', '#b0c5df', '#83cfff')}[theme]
    bg, border, ink, muted, accent = palette
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title">'
            f'<title id="title">{escape(title)}</title>'
            f'<rect x=".5" y=".5" width="{width-1}" height="{height-1}" rx="12" fill="{bg}" stroke="{border}"/>'
            '<g font-family="Segoe UI, Helvetica, Arial, sans-serif">' +
            text(24, 36, title, accent, 19, 600) + content(ink, muted, accent) + '</g></svg>\n')


def render(snapshot, theme):
    def stats(ink, muted, accent):
        rows = [('Public commits · past year', snapshot['public_commits']), ('Public repositories', snapshot['repositories']),
                ('Merged upstream PRs', snapshot['upstream_merged']), ('Open upstream PRs', snapshot['upstream_open'])]
        return ''.join(text(24, 79 + i * 34, label, muted) + text(372, 79 + i * 34, f'{value:,}', ink, 19, 600, 'end')
                       for i, (label, value) in enumerate(rows)) + text(24, 229, 'Public work · refreshed daily', muted, 11)

    def languages(ink, muted, accent):
        rows = snapshot['languages']
        total = sum(r['bytes'] for r in rows)
        shown = rows[:5]
        if len(rows) > 5:
            shown = shown + [{'name': 'Other', 'bytes': sum(r['bytes'] for r in rows[5:]), 'color': '#64748b'}]
        if not total:
            return text(24, 100, 'No public language data available', muted)
        parts, x = [], 24
        for row in shown:
            color = row['color'] if re.fullmatch(r'#[0-9a-fA-F]{6}', row['color']) else '#64748b'
            width = 352 * row['bytes'] / total
            parts.append(f'<rect x="{x:.3f}" y="58" width="{width:.3f}" height="12" fill="{color}"/>')
            x += width
        for i, row in enumerate(shown):
            x, y = 24 + (i % 2) * 185, 105 + (i // 2) * 37
            name = row['name'] if len(row['name']) <= 17 else row['name'][:16] + '…'
            color = row['color'] if re.fullmatch(r'#[0-9a-fA-F]{6}', row['color']) else '#64748b'
            parts.append(f'<circle cx="{x+5}" cy="{y-5}" r="4" fill="{color}"/>' +
                         text(x + 15, y, name, ink, 12) + text(x + 15, y + 16, f'{100 * row["bytes"] / total:.1f}%', muted, 11))
        return ''.join(parts) + text(24, 229, 'Code bytes · owned public repositories', muted, 11)

    def activity(ink, muted, accent):
        values = [(snapshot['calendar_contributions'], 'Contributions', 'Past year'),
                  (snapshot['streaks']['current'], 'Current streak', 'Days · today or yesterday active'),
                  (snapshot['streaks']['longest'], 'Longest streak', 'Days · within the past year')]
        parts = []
        for i, (value, label, note) in enumerate(values):
            x = 136 + i * 272
            if i:
                parts.append(f'<path d="M{i*272} 65v95" stroke="{muted}" opacity=".25"/>')
            parts.extend([text(x, 102, f'{value:,}', accent if i == 1 else ink, 36, 700, 'middle'),
                          text(x, 132, label, ink, 16, 600, 'middle'),
                          text(x, 157, note, muted, 11, anchor='middle')])
        return ''.join(parts) + text(408, 192, f'{snapshot["period_start"]} — {snapshot["period_end"]} · GitHub calendar · UTC', muted, 11, anchor='middle')

    def activity_mobile(ink, muted, accent):
        values = [(snapshot['calendar_contributions'], 'Contributions', 'Past year'),
                  (snapshot['streaks']['current'], 'Current streak', 'Days · today or yesterday active'),
                  (snapshot['streaks']['longest'], 'Longest streak', 'Days · within the past year')]
        parts = []
        for i, (value, label, note) in enumerate(values):
            y = 80 + i * 75
            parts.extend([text(24, y, label, ink, 16, 600), text(24, y + 21, note, muted, 11),
                          text(376, y + 12, f'{value:,}', accent if i == 1 else ink, 30, 700, 'end')])
        return ''.join(parts) + text(24, 302, f'{snapshot["period_start"]} — {snapshot["period_end"]} · UTC', muted, 11)

    return {'stats': card('GitHub at a glance', 400, 250, stats, theme),
            'languages': card('Languages in my repositories', 400, 250, languages, theme),
            'activity': card('A year of building', 816, 214, activity, theme),
            'activity-mobile': card('A year of building', 400, 330, activity_mobile, theme)}


def publish(snapshot):
    assets = {f'{name}-{theme}.svg': svg for theme in ('light', 'dark')
              for name, svg in render(snapshot, theme).items()}
    for svg in assets.values():
        ET.fromstring(svg)
    for name, svg in assets.items():
        (ROOT / 'assets' / name).write_text(svg, encoding='utf-8')
    (ROOT / 'data/profile-cards.json').write_text(json.dumps(snapshot, indent=2) + '\n', encoding='utf-8')
    print(f'Updated cards for {snapshot["owner"]}: {snapshot["repositories"]} repositories, '
          f'{snapshot["stars"]} stars, {snapshot["calendar_contributions"]} calendar contributions.')


if __name__ == '__main__':
    owner = os.getenv('PROFILE_OWNER', 'cristiangirlea')
    if not re.fullmatch(r'[A-Za-z0-9-]+', owner):
        raise ValueError('Invalid GitHub username')
    publish(collect(owner))
