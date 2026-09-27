import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('refresh', Path(__file__).with_name('refresh-profile.py'))
refresh = importlib.util.module_from_spec(spec)
spec.loader.exec_module(refresh)


def pr(identifier, repo='PostHog/posthog-go', title='Add reusable flush', merged=True):
    return {'id': identifier, 'repository_url': 'https://api.github.com/repos/' + repo,
            'title': title, 'user': {'login': 'cristiangirlea'},
            'pull_request': {'merged_at': '2026-09-22T13:32:56Z' if merged else None}}


class Counts(unittest.TestCase):
    def test_exclusions_and_deduplication(self):
        items = [pr(1), pr(1), pr(2, 'HeRAMS-WHO/herams-backend'),
                 pr(3, 'cristiangirlea/tidedesk'), pr(4, title='[Snyk] Update dependency')]
        self.assertEqual(refresh.count_repositories(items, 'cristiangirlea'), {'PostHog/posthog-go': 1})

    def test_unmerged_is_rejected(self):
        with self.assertRaises(ValueError):
            refresh.count_repositories([pr(1, merged=False)], 'cristiangirlea')

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
