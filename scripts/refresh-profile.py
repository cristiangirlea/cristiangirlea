"""Refresh the public upstream contribution audit."""
import json
import os
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
# Profile exclusions apply to discovery AND counting so refreshes cannot restore them.
EXCLUDED_ORGS = {'herams-who', 'yiisoft'}


def api(path):
    headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'github-profile-refresh'}
    if os.getenv('GH_TOKEN'):
        headers['Authorization'] = 'Bearer ' + os.environ['GH_TOKEN']
    with urlopen(Request('https://api.github.com/' + path, headers=headers), timeout=30) as response:
        return json.load(response)


def gerrit_changes(repo, number):
    query = urlencode([('q', f'project:{repo.split("/")[1]} message:"GitHub-Pull-Request: {repo}#{number}"'),
                       ('o', 'CURRENT_REVISION'), ('o', 'CURRENT_COMMIT')])
    with urlopen('https://go-review.googlesource.com/changes/?' + query, timeout=30) as response:
        return json.loads(response.read().decode().split('\n', 1)[1])


def resolve_gerrit(items):
    """Match the exact imported PR trailer; GitHub's merge flag misses Gerrit."""
    for item in items:
        repo = item['repository_url'].removeprefix('https://api.github.com/repos/')
        if not repo.startswith('golang/'):
            continue
        matches = []
        for change in gerrit_changes(repo, item['number']):
            message = change['revisions'][change['current_revision']]['commit']['message']
            trailer = f'GitHub-Pull-Request: {repo}#{item["number"]}'
            if change['project'] == repo.split('/')[1] and trailer in message.splitlines():
                matches.append(change)
        if len(matches) > 1:
            raise ValueError('Ambiguous Gerrit import')
        if matches:
            change = matches[0]
            states = {'MERGED': 'merged', 'NEW': 'open', 'ABANDONED': 'closed'}
            item['upstream_state'] = states[change['status']]
            item['gerrit_url'] = f'https://go-review.googlesource.com/c/{change["project"]}/+/{change["_number"]}'
        elif item['state'] == 'closed' and not item['pull_request'].get('merged_at'):
            raise ValueError('Closed Go PR has no verified Gerrit status')


def count_repositories(items, owner):
    counts = {}
    seen = set()
    for item in items:
        repo = item['repository_url'].removeprefix('https://api.github.com/repos/')
        if item['id'] in seen:
            continue
        seen.add(item['id'])
        if item['user']['login'].lower() != owner.lower():
            raise ValueError('Search returned an unexpected author')
        if 'pull_request' not in item:
            raise ValueError('Search returned an issue rather than a pull request')
        if repo.split('/')[0].lower() in {owner.lower(), *EXCLUDED_ORGS} or item['title'].startswith('[Snyk]'):
            continue
        state = item.get('upstream_state') or ('merged' if item['pull_request'].get('merged_at') else item['state'])
        if state not in {'merged', 'open', 'closed'}:
            raise ValueError('Unknown pull request state')
        counts.setdefault(repo, Counter())[state] += 1
        if state == 'open' and item.get('draft'):
            counts[repo]['draft'] += 1
    return counts


def verify_closed_prs(items):
    """Use PR detail records for acceptance, rather than search indexing alone."""
    for item in items:
        repo = item['repository_url'].removeprefix('https://api.github.com/repos/')
        if repo.startswith('golang/') or item['state'] != 'closed':
            continue
        detail = api(f'repos/{repo}/pulls/{item["number"]}')
        if detail['user']['login'].lower() != item['user']['login'].lower():
            raise ValueError('Pull request author mismatch')
        item['state'] = detail['state']
        item['draft'] = detail.get('draft', False)
        item['pull_request']['merged_at'] = detail['merged_at']


def collect(owner):
    query = f'author:{owner} is:pr is:public -user:{owner}' + ''.join(f' -org:{org}' for org in sorted(EXCLUDED_ORGS))
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
    verify_closed_prs(items)
    resolve_gerrit(items)
    counts = count_repositories(items, owner)
    repos = []
    for name, count in sorted(counts.items()):
        meta = api('repos/' + name)
        if meta['private']:
            raise ValueError('Unexpected private repository')
        if meta['fork']:
            continue
        evidence = [{'pr': item['html_url'], 'number': item['number'], 'state': item['upstream_state'], 'url': item['gerrit_url']}
                    for item in items if item.get('gerrit_url') and item['repository_url'].endswith('/' + name)]
        merged_prs = [{'pr': item['html_url'], 'evidence': item.get('gerrit_url', item['html_url'])}
                      for item in items if item['repository_url'].endswith('/' + name)
                      and (item.get('upstream_state') == 'merged' or item['pull_request'].get('merged_at'))]
        repos.append({'name': name, **{state: count[state] for state in ('merged', 'open', 'closed', 'draft')}, 'stars': meta['stargazers_count'], 'gerrit': evidence, 'merged_prs': merged_prs})
    return sorted(repos, key=lambda r: (-r['stars'], r['name'].lower()))


def publish(repos, owner):
    """Keep the contribution audit without adding PR totals to the profile."""
    stamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    (ROOT / 'data').mkdir(exist_ok=True)
    (ROOT / 'data' / 'contributions.json').write_text(
        json.dumps({'checked_at': stamp, 'owner': owner, 'repositories': repos}, indent=2) + '\n', encoding='utf-8')
    print(f'Refreshed the contribution audit across {len(repos)} public repositories.')


if __name__ == '__main__':
    owner = os.getenv('PROFILE_OWNER', 'cristiangirlea')
    if not re.fullmatch(r'[A-Za-z0-9-]+', owner):
        raise ValueError('Invalid GitHub username')
    publish(collect(owner), owner)
