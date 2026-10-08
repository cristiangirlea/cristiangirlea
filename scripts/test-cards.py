import importlib.util
from datetime import date
from pathlib import Path
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

spec = importlib.util.spec_from_file_location('cards', Path(__file__).with_name('refresh-cards.py'))
cards = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cards)


class Cards(unittest.TestCase):
    def test_current_streak_survives_a_quiet_today(self):
        days = [{'date': '2026-10-07', 'contributionCount': 2},
                {'date': '2026-10-08', 'contributionCount': 1},
                {'date': '2026-10-09', 'contributionCount': 0}]
        self.assertEqual(cards.streaks(days, date(2026, 10, 9)), {'current': 2, 'longest': 2})
        days[-2]['contributionCount'] = 0
        self.assertEqual(cards.streaks(days, date(2026, 10, 9)), {'current': 0, 'longest': 1})

    def test_active_today_and_calendar_gaps(self):
        days = [{'date': '2026-10-07', 'contributionCount': 0},
                {'date': '2026-10-08', 'contributionCount': 2},
                {'date': '2026-10-09', 'contributionCount': 1}]
        self.assertEqual(cards.streaks(days, date(2026, 10, 9)), {'current': 2, 'longest': 2})
        with self.assertRaises(ValueError):
            cards.streaks([days[0], days[2]], date(2026, 10, 9))

    def test_graphql_errors_do_not_publish_partial_totals(self):
        import io
        with patch.dict(cards.os.environ, {'GH_TOKEN': 'test'}), \
                patch.object(cards, 'urlopen', return_value=io.BytesIO(b'{"errors":[{"message":"denied"}]}')):
            with self.assertRaises(ValueError):
                cards.graphql({})

    def test_cards_are_valid_svg_with_clear_scopes_and_escaped_languages(self):
        snapshot = {'stars': 15, 'public_commits': 90, 'repositories': 6, 'upstream_merged': 10, 'upstream_open': 41,
                    'languages': [{'name': 'C++ & C#', 'bytes': 100, 'color': '#245bcc'}],
                    'calendar_contributions': 100, 'streaks': {'current': 2, 'longest': 10},
                    'period_start': '2025-10-10', 'period_end': '2026-10-09'}
        for theme in ('light', 'dark'):
            rendered = cards.render(snapshot, theme)
            for svg in rendered.values():
                ET.fromstring(svg)
            self.assertIn('C++ &amp; C#', rendered['languages'])
            self.assertIn('100.0%', rendered['languages'])
            self.assertIn('within the past year', rendered['activity'])
            self.assertIn('Merged upstream PRs', rendered['stats'])


if __name__ == '__main__':
    unittest.main()
