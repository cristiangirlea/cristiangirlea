import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('refresh', Path(__file__).with_name('refresh-profile.py'))
refresh = importlib.util.module_from_spec(spec)
spec.loader.exec_module(refresh)


def pr(identifier, repo='PostHog/posthog-go', title='Add reusable flush', merged=True, state='closed', draft=False):
    return {'id': identifier, 'repository_url': 'https://api.github.com/repos/' + repo,
            'title': title, 'user': {'login': 'cristiangirlea'}, 'state': state, 'draft': draft,
            'pull_request': {'merged_at': '2026-09-22T13:32:56Z' if merged else None}}


class Counts(unittest.TestCase):
    def test_exclusions_and_deduplication(self):
        items = [pr(1), pr(1), pr(2, 'HeRAMS-WHO/herams-backend'),
                 pr(3, 'cristiangirlea/tidedesk'), pr(4, title='[Snyk] Update dependency')]
        self.assertEqual(refresh.count_repositories(items, 'cristiangirlea'), {'PostHog/posthog-go': {'merged': 1}})

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


if __name__ == '__main__':
    unittest.main()
