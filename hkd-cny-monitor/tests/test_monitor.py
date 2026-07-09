import unittest
from datetime import date, timedelta
from pathlib import Path
import sys


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from monitor import DEFAULT_CONFIG, analyze_points  # noqa: E402


def make_points(rates):
    start = date(2026, 1, 1)
    return [
        {"date": (start + timedelta(days=index)).isoformat(), "rate": rate}
        for index, rate in enumerate(rates)
    ]


class MonitorAnalysisTests(unittest.TestCase):
    def test_alert_when_latest_is_near_recent_high(self):
        rates = [0.8800, 0.8810, 0.8825, 0.8840, 0.8860, 0.8880, 0.8895, 0.8900]
        config = dict(DEFAULT_CONFIG, lookback_days=20, near_high_threshold_pct=0.3, alert_min_percentile=90)

        result = analyze_points(make_points(rates), config, "test")

        self.assertEqual(result["signals"]["status"], "alert")
        self.assertTrue(result["signals"]["alert"])
        self.assertEqual(result["window"]["high_rate"], 0.89)

    def test_wait_when_latest_is_well_below_recent_high(self):
        rates = [0.8800, 0.9000, 0.9200, 0.9150, 0.9050, 0.8950, 0.8900, 0.8880]
        config = dict(DEFAULT_CONFIG, lookback_days=20, near_high_threshold_pct=0.3, alert_min_percentile=90)

        result = analyze_points(make_points(rates), config, "test")

        self.assertEqual(result["signals"]["status"], "wait")
        self.assertFalse(result["signals"]["alert"])
        self.assertGreater(result["window"]["distance_to_high_pct"], 0.3)

    def test_target_rate_can_trigger_even_if_percentile_rule_does_not(self):
        rates = [0.8800, 0.8850, 0.8860, 0.8840, 0.8870, 0.8865, 0.8868, 0.8871]
        config = dict(
            DEFAULT_CONFIG,
            lookback_days=20,
            near_high_threshold_pct=0.01,
            alert_min_percentile=100,
            target_rate=0.887,
        )

        result = analyze_points(make_points(rates), config, "test")

        self.assertTrue(result["signals"]["target_hit"])
        self.assertTrue(result["signals"]["alert"])


if __name__ == "__main__":
    unittest.main()
