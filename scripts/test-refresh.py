import importlib.util
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('refresh', Path(__file__).with_name('refresh-profile.py'))
refresh = importlib.util.module_from_spec(spec)
spec.loader.exec_module(refresh)


def pr(identifier, repo='PostHog/posthog-go', title='Add reusable flush', merged=True, state='closed', draft=False):
    return {'id': identifier, 'repository_url': 'https://api.github.com/repos/' + repo,
            'title': title, 'user': {'login': 'cristiangirlea'}, 'state': state, 'draft': draft,
            'pull_request': {'merged_at': '2026-09-22T13:32:56Z' if merged else None}}


class Counts(unittest.TestCase):
    def test_gerrit_status_overrides_github_closed_flag(self):
        for status, expected in [('MERGED', 'merged'), ('NEW', 'open'), ('ABANDONED', 'closed')]:
            with self.subTest(status=status):
                item = pr(1, 'golang/go', merged=False)
                item['number'] = 81562
                change = {'project': 'go', '_number': 833584, 'status': status,
                          'current_revision': 'abc', 'revisions': {'abc': {'commit': {
                              'message': 'Fix\n\nGitHub-Pull-Request: golang/go#81562\n'}}}}
                with patch.object(refresh, 'gerrit_changes', return_value=[change]):
                    refresh.resolve_gerrit([item])
                self.assertEqual(refresh.count_repositories([item], 'cristiangirlea'),
                                 {'golang/go': {expected: 1}})

    def test_gerrit_requires_exact_pr_trailer(self):
        item = pr(1, 'golang/go', merged=False)
        item['number'] = 81562
        change = {'project': 'go', '_number': 833584, 'status': 'MERGED',
                  'current_revision': 'abc', 'revisions': {'abc': {'commit': {
                      'message': 'GitHub-Pull-Request: golang/go#815620\n'}}}}
        with patch.object(refresh, 'gerrit_changes', return_value=[change]):
            with self.assertRaises(ValueError):
                refresh.resolve_gerrit([item])

    def test_exclusions_and_deduplication(self):
        items = [pr(1), pr(1), pr(2, 'HeRAMS-WHO/herams-backend'),
                 pr(3, 'cristiangirlea/tidedesk'), pr(4, title='[Snyk] Update dependency'),
                 pr(5, 'yiisoft/yii2-framework'), pr(6, 'Yiisoft/yii2', merged=False, state='open')]
        self.assertEqual(refresh.count_repositories(items, 'cristiangirlea'), {'PostHog/posthog-go': {'merged': 1}})

    def test_pr_detail_corrects_stale_search_merge_status(self):
        item = pr(1, merged=False)
        item['number'] = 324
        detail = {'user': item['user'], 'state': 'closed', 'merged_at': '2026-09-22T13:32:56Z'}
        with patch.object(refresh, 'api', return_value=detail):
            refresh.verify_closed_prs([item])
        self.assertEqual(refresh.count_repositories([item], 'cristiangirlea'),
                         {'PostHog/posthog-go': {'merged': 1}})

    def test_statuses_stay_separate_and_drafts_are_open(self):
        items = [pr(1), pr(2, merged=False), pr(3, merged=False, state='open'),
                 pr(4, merged=False, state='open', draft=True)]
        self.assertEqual(refresh.count_repositories(items, 'cristiangirlea'),
                         {'PostHog/posthog-go': {'merged': 1, 'closed': 1, 'open': 2, 'draft': 1}})

    def test_incomplete_search_is_rejected(self):
        old = refresh.api
        try:
            refresh.api = lambda _: {'incomplete_results': True, 'total_count': 1, 'items': [pr(1)]}
            with self.assertRaises(ValueError):
                refresh.collect('cristiangirlea')
        finally:
            refresh.api = old

    def test_fork_targets_are_excluded_from_the_audit(self):
        item = pr(1, 'other-user/fork', merged=False, state='open')
        with patch.object(refresh, 'api', side_effect=[
                {'total_count': 1, 'items': [item]},
                {'private': False, 'fork': True}]):
            self.assertEqual(refresh.collect('cristiangirlea'), [])

    def test_profile_highlights_merged_and_open_but_preserves_closed_audit(self):
        repos = [
            {'name': 'laravel/octane', 'merged': 1, 'open': 0, 'closed': 1,
             'draft': 0, 'stars': 4000},
            {'name': 'example/active', 'merged': 0, 'open': 2, 'closed': 0,
             'draft': 1, 'stars': 100},
            {'name': 'example/closed-only', 'merged': 0, 'open': 0, 'closed': 3,
             'draft': 0, 'stars': 200}]
        with TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'README.md').write_text(
                '<img src="assets/merged-small.svg?v=7">\n' +
                refresh.START + '\nold\n' + refresh.END, encoding='utf-8')
            with patch.object(refresh, 'ROOT', root):
                refresh.publish(repos, 'cristiangirlea')
            readme = (root / 'README.md').read_text(encoding='utf-8')
            self.assertNotIn('Closed, unmerged', readme)
            self.assertNotIn('example/closed-only', readme)
            self.assertNotIn('submitted-prs.svg', readme)
            self.assertIn('laravel/octane', readme)
            self.assertIn('1 merged pull requests', readme)
            self.assertIn('2 open pull requests', readme)
            self.assertIn('2 public upstream repositories', readme)
            self.assertIn('assets/merged-small.svg?v=1', readme)
            self.assertIn('Open includes 1 drafts', readme)
            audit = json.loads((root / 'data/contributions.json').read_text(encoding='utf-8'))
            self.assertEqual(audit['repositories'], repos)
            self.assertIn('MERGED PRs: 1'.upper(),
                          (root / 'assets/merged-prs.svg').read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
