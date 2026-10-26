"""Unit tests for batch queue processor."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from igprompts.batch import TopicItem, load_topic_queue, run_batch_queue
from igprompts.providers import DryRunProvider, ManualProvider


class TestBatch(unittest.TestCase):
    def test_load_json_queue(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            json_file = Path(tmp_dir) / "queue.json"
            data = [
                {"id": "01", "topic": "主題一", "niche": "賽道A", "series": "faceless"},
                {"id": "02", "topic": "主題二", "niche": "賽道B", "series": "reels"},
            ]
            json_file.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

            items = load_topic_queue(json_file)
            self.assertEqual(len(items), 2)
            self.assertEqual(items[0].id, "01")
            self.assertEqual(items[0].topic, "主題一")
            self.assertEqual(items[0].series, "faceless_carousel")
            self.assertEqual(items[1].series, "short_video_reels")

    def test_load_csv_queue(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            csv_file = Path(tmp_dir) / "queue.csv"
            lines = [
                "id,topic,niche,audience,series",
                "C01,CSV主題一,AI應用,職場新鮮人,faceless",
                "C02,CSV主題二,程式開發,轉職者,reels",
            ]
            csv_file.write_text("\n".join(lines), encoding="utf-8-sig")

            items = load_topic_queue(csv_file)
            self.assertEqual(len(items), 2)
            self.assertEqual(items[0].id, "C01")
            self.assertEqual(items[0].topic, "CSV主題一")
            self.assertEqual(items[0].audience, "職場新鮮人")

    def test_invalid_queue_raises(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            bad_ext = Path(tmp_dir) / "bad.txt"
            bad_ext.write_text("hello", encoding="utf-8")
            with self.assertRaises(ValueError):
                load_topic_queue(bad_ext)

            not_found = Path(tmp_dir) / "not_found.json"
            with self.assertRaises(FileNotFoundError):
                load_topic_queue(not_found)

    def test_run_batch_queue(self):
        items = [
            TopicItem(id="B1", topic="測試批次1", niche="測試領域", series="faceless_carousel"),
            TopicItem(id="B2", topic="測試批次2", niche="測試領域", series="short_video_reels"),
        ]
        with tempfile.TemporaryDirectory() as tmp_dir:
            results = run_batch_queue(items, tmp_dir, provider=DryRunProvider())
            self.assertEqual(len(results), 2)
            self.assertEqual(results[0]["id"], "B1")
            self.assertTrue(Path(results[0]["manifest"]).exists())
            self.assertTrue(Path(results[1]["manifest"]).exists())

    def test_manual_provider_handoff_is_isolated_per_topic(self):
        items = [
            TopicItem(id="B1", topic="t1", niche="AAA", series="faceless_carousel"),
            TopicItem(id="B2", topic="t2", niche="BBB", series="faceless_carousel"),
        ]
        with tempfile.TemporaryDirectory() as tmp_dir:
            handoff = Path(tmp_dir) / "handoff"
            run_batch_queue(items, tmp_dir, provider=ManualProvider(handoff))
            p1 = handoff / "B1_faceless_carousel" / "01-niche_ideation.prompt.md"
            p2 = handoff / "B2_faceless_carousel" / "01-niche_ideation.prompt.md"
            self.assertIn("AAA", p1.read_text(encoding="utf-8"))
            self.assertIn("BBB", p2.read_text(encoding="utf-8"))

    def test_duplicate_ids_rejected(self):
        items = [TopicItem(id="X", topic="a"), TopicItem(id="X", topic="b")]
        with tempfile.TemporaryDirectory() as tmp_dir:
            with self.assertRaises(ValueError):
                run_batch_queue(items, tmp_dir, provider=DryRunProvider())
            queue = Path(tmp_dir) / "q.json"
            queue.write_text(json.dumps([{"id": "X", "topic": "a"}, {"id": "X", "topic": "b"}]), encoding="utf-8")
            with self.assertRaises(ValueError):
                load_topic_queue(queue)

    def test_unsafe_ids_rejected(self):
        for bad in ("../evil", "a/b", "a\b", "..", "C:x"):
            with self.subTest(bad=bad), tempfile.TemporaryDirectory() as tmp_dir:
                with self.assertRaises(ValueError):
                    run_batch_queue([TopicItem(id=bad, topic="a")], tmp_dir, provider=DryRunProvider())
                self.assertEqual([p.name for p in Path(tmp_dir).iterdir()], [])


if __name__ == "__main__":
    unittest.main()
