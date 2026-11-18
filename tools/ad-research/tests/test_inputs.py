from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from ad_research.inputs import attach_metrics, load_records


CATALOG = """id,niche,market,kind,title,platform,purchases,first_seen,last_seen
one,food,US,ad,Demo,Facebook,999,2026-11-01,2026-11-17
"""
METRICS_HEADER = "id,market,platform,period_start,period_end,attribution,currency,spend,purchases,revenue\n"
METRIC = "one,US,facebook,2026-11-01,2026-11-17,7d_click,USD,90,3,180\n"


class MetricsTests(unittest.TestCase):
    def setUp(self):
        temp = TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        catalog = self.root / "ads.csv"
        catalog.write_text(CATALOG, encoding="utf-8")
        self.records = load_records(catalog)

    def attach(self, metrics):
        path = self.root / "metrics.csv"
        path.write_text(METRICS_HEADER + metrics, encoding="utf-8")
        return list(attach_metrics(self.records, path))

    def test_separates_public_metadata_and_observed_purchases(self):
        self.assertNotIn("purchases", self.records["one"])
        row, = self.attach(METRIC)
        self.assertEqual((row["purchases"], row["spend"], row["revenue"]), (3, 90, 180))

    def test_rejects_mismatched_scope(self):
        with self.assertRaisesRegex(ValueError, "mercado e plataforma"):
            self.attach(METRIC.replace("facebook", "instagram"))

    def test_rejects_duplicate_measurement(self):
        with self.assertRaisesRegex(ValueError, "duplicada"):
            self.attach(METRIC * 2)

    def test_keeps_missing_distinct_from_zero(self):
        zero, = self.attach(METRIC.replace(",3,180", ",0,"))
        self.assertEqual(zero["purchases"], 0)
        self.assertIsNone(zero["revenue"])
