"""Refresh public upstream contribution counts, badges and README table."""
import json
import os
import re
from collections import Counter
from datetime import datetime, timezone
from html import escape
from pathlib import Path
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
START, END = '<!-- merged-prs:start -->', '<!-- merged-prs:end -->'
EXCLUDED_ORGS = {'herams-who'}


def api(path):
    headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'github-profile-refresh'}
    if os.getenv('GH_TOKEN'):
        headers['Authorization'] = 'Bearer ' + os.environ['GH_TOKEN']
    with urlopen(Request('https://api.github.com/' + path, headers=headers), timeout=30) as response:
        return json.load(response)


def count_repositories(items, owner):
    counts = Counter()
    seen = set()
    for item in items:
        repo = item['repository_url'].removeprefix('https://api.github.com/repos/')
        if item['id'] in seen:
            continue
        seen.add(item['id'])
        if item['user']['login'].lower() != owner.lower():
            raise ValueError('Search returned an unexpected author')
        if not item.get('pull_request', {}).get('merged_at'):
            raise ValueError('Search returned an unmerged pull request')
        if repo.split('/')[0].lower() in {owner.lower(), *EXCLUDED_ORGS} or item['title'].startswith('[Snyk]'):
            continue
        counts[repo] += 1
    return counts


def collect(owner):
    query = f'author:{owner} is:pr is:merged is:public -user:{owner}' + ''.join(f' -org:{org}' for org in sorted(EXCLUDED_ORGS))
    items = []
    expected = None
    for page in range(1, 11):
        result = api('search/issues?' + urlencode({'q': query, 'per_page': 100, 'page': page, 'sort': 'created', 'order': 'asc'}))
        if result.get('incomplete_results') or result['total_count'] > 1000:
            raise ValueError('Incomplete search; refusing to publish partial totals')
        if expected is None:
            expected = result['total_count']
        if result['total_count'] != expected:
            raise ValueError('Search changed during pagination; retry the workflow')
        items.extend(result['items'])
        if len(items) >= expected:
            break
        if not result['items']:
            raise ValueError('Search pagination ended early')
    if len({item['id'] for item in items}) != expected:
        raise ValueError('Missing or duplicated search results; refusing partial totals')
    counts = count_repositories(items, owner)
    repos = []
    for name, count in sorted(counts.items(), key=lambda x: (-x[1], x[0].lower())):
        meta = api('repos/' + name)
        if meta['private']:
            raise ValueError('Unexpected private repository')
        repos.append({'name': name, 'merged': count, 'stars': meta['stargazers_count']})
    return repos


def badge(label, value, color, large=False):
    height, font = (28, 11) if large else (20, 11)
    label = label.upper() if large else label
    left = round(len(label) * 7.4 + 22)
    right = max(34, round(len(str(value)) * 7.5 + 22))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{left+right}" height="{height}" role="img" aria-label="{escape(label)}: {value}">
<title>{escape(label)}: {value}</title><path fill="#555" d="M0 0h{left}v{height}H0z"/><path fill="#{color}" d="M{left} 0h{right}v{height}H{left}z"/>
<g fill="#fff" text-anchor="middle" font-family="Verdana,DejaVu Sans,sans-serif" font-size="{font}"><text x="{left/2}" y="{height/2+4}">{escape(label)}</text><text x="{left+right/2}" y="{height/2+4}" font-weight="bold">{value}</text></g></svg>\n'''


def publish(repos, owner):
    readme_path = ROOT / 'README.md'
    readme = readme_path.read_text(encoding='utf-8')
    if readme.count(START) != 1 or readme.count(END) != 1:
        raise ValueError('README must have exactly one contribution block')
    total = sum(r['merged'] for r in repos)
    stars = sum(r['stars'] for r in repos)
    badges = {'merged-prs.svg': badge('Merged PRs', total, '8250DF', True),
              'projects.svg': badge('Repositories', len(repos), '0969DA', True),
              'upstream-stars.svg': badge('Upstream stars', stars, '9D7209', True),
              'merged-small.svg': badge('Upstream merged PRs', total, '8250DF')}
    stamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    rows = []
    for repo in repos:
        name = escape(repo['name'])
        # Link the numeric count to the broad author/merged query. The documented
        # Snyk title exclusion is applied by this script, not a brittle search token.
        search = 'https://github.com/' + repo['name'] + '/pulls?' + urlencode({'q': f'is:pr is:merged author:{owner}'})
        rows.append(f'<tr><td><a href="https://github.com/{name}"><code>{name}</code></a></td><td align="right">{repo["stars"]}</td><td align="right"><a href="{escape(search, quote=True)}">{repo["merged"]}</a></td></tr>')
    block = '\n'.join([START, '<p align="center">',
        f'  <img src="assets/merged-prs.svg" alt="{total} merged pull requests">',
        f'  <img src="assets/projects.svg" alt="{len(repos)} public upstream repositories">',
        f'  <img src="assets/upstream-stars.svg" alt="{stars} combined stars on those upstream repositories">',
        '</p>', '<table>', '<thead><tr><th>Project</th><th>★</th><th>Merged</th></tr></thead>',
        '<tbody>', *rows, '</tbody></table>',
        f'<p><sub>Selected public upstream contributions, merged PRs only. Stars belong to the upstream repositories. <a href="scripts/refresh-profile.py">Selection rules</a> · Refreshed {stamp} by <a href=".github/workflows/refresh.yml">GitHub Actions</a>.</sub></p>', END])
    updated = re.sub(re.escape(START) + r'.*?' + re.escape(END), lambda _: block, readme, flags=re.S)
    # Validate everything before replacing the previous published snapshot.
    (ROOT / 'assets').mkdir(exist_ok=True)
    for name, contents in badges.items():
        (ROOT / 'assets' / name).write_text(contents, encoding='utf-8')
    (ROOT / 'data').mkdir(exist_ok=True)
    (ROOT / 'data' / 'contributions.json').write_text(json.dumps({'checked_at': stamp, 'owner': owner, 'repositories': repos}, indent=2) + '\n', encoding='utf-8')
    readme_path.write_text(updated, encoding='utf-8')
    print(f'Refreshed {total} merged PRs across {len(repos)} public repositories.')


if __name__ == '__main__':
    owner = os.getenv('PROFILE_OWNER', 'cristiangirlea')
    if not re.fullmatch(r'[A-Za-z0-9-]+', owner):
        raise ValueError('Invalid GitHub username')
    publish(collect(owner), owner)
