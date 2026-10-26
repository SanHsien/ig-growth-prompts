"""Unit tests for 7-day experiment ledger and reports."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from igprompts.experiments import (
    LedgerError,
    build_report,
    load_ledger,
    write_plan,
)


class TestExperiments(unittest.TestCase):
    def test_write_and_load_empty_plan(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            csv_path = Path(tmp_dir) / "test_ledger.csv"
            write_plan(csv_path, days=7)
            self.assertTrue(csv_path.exists())

            rows = load_ledger(csv_path)
            self.assertEqual(len(rows), 7)
            self.assertEqual(rows[0].day, "1")
            self.assertIsNone(rows[0].metric("views"))

    def test_metric_calculation(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            csv_path = Path(tmp_dir) / "data.csv"
            write_plan(csv_path, days=2)

            # Inject test data
            lines = [
                "day,hypothesis,topic,hook,format,cta,primary_metric,views,saves,shares,comments,profile_visits,follows,avg_watch_pct",
                "1,Hypothesis A,Topic 1,Hook 1,Reel,CTA 1,save_rate,1000,50,20,10,30,5,45.5",
                "2,Hypothesis B,Topic 2,Hook 2,Carousel,CTA 2,share_rate,2000,60,80,15,40,10,55.0",
            ]
            csv_path.write_text("\n".join(lines), encoding="utf-8-sig")

            rows = load_ledger(csv_path)
            self.assertEqual(len(rows), 2)

            # Test calculations
            self.assertEqual(rows[0].metric("views"), 1000.0)
            self.assertAlmostEqual(rows[0].metric("save_rate"), 0.05)
            self.assertAlmostEqual(rows[0].metric("share_rate"), 0.02)
            self.assertEqual(rows[0].metric("avg_watch_pct"), 45.5)

            report = build_report(rows)
            self.assertIn("# 7 天測試報告", report)
            self.assertIn("最高 Day 2", report)
            self.assertIn("可以確定的結論", report)

    def test_invalid_number_raises(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            csv_path = Path(tmp_dir) / "invalid.csv"
            lines = [
                "day,hypothesis,topic,hook,format,cta,primary_metric,views,saves,shares,comments,profile_visits,follows,avg_watch_pct",
                "1,Hypothesis,Topic,Hook,Format,CTA,views,not_a_number,,,,,,",
            ]
            csv_path.write_text("\n".join(lines), encoding="utf-8-sig")
            with self.assertRaises(LedgerError):
                load_ledger(csv_path)


    def test_non_finite_numbers_rejected(self):
        header = "day,hypothesis,topic,hook,format,cta,primary_metric,views,saves,shares,comments,profile_visits,follows,avg_watch_pct"
        for bad in ("nan", "inf", "-inf", "Infinity"):
            with self.subTest(bad=bad), tempfile.TemporaryDirectory() as tmp_dir:
                csv_path = Path(tmp_dir) / "ledger.csv"
                csv_path.write_text(f"{header}\n1,H,T,Hk,F,C,views,{bad},,,,,,\n", encoding="utf-8-sig")
                with self.assertRaises(LedgerError):
                    load_ledger(csv_path)


    def test_report_table_survives_pipes_and_newlines(self):
        import re
        header = "day,hypothesis,topic,hook,format,cta,primary_metric,views,saves,shares,comments,profile_visits,follows,avg_watch_pct"
        with tempfile.TemporaryDirectory() as tmp_dir:
            csv_path = Path(tmp_dir) / "ledger.csv"
            csv_path.write_text(
                f'{header}\n1,"A | B\nsecond line",T,H,"Reel | Short",C,views,100,5,1,1,1,1,50\n',
                encoding="utf-8-sig",
            )
            report = build_report(load_ledger(csv_path))
        table = [ln for ln in report.splitlines() if ln.startswith("|")]
        self.assertEqual(len(table), 3)  # header, separator, one data row
        cells = [len(re.split(r"(?<!\\)\|", ln)) for ln in table]
        self.assertEqual(len(set(cells)), 1, table)


if __name__ == "__main__":
    unittest.main()
