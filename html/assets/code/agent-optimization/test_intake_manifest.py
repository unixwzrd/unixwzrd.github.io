#!/usr/bin/env python3
"""Canary tests for the Post 2A intake manifest utility."""

from __future__ import annotations

import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import intake_manifest
from intake_manifest import inventory


class IntakeManifestTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name) / "sources"
        self.root.mkdir()
        self.database = Path(self.temporary.name) / "manifest.db"

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def write(self, relative: str, content: str) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        return path

    def test_new_unchanged_and_changed_are_one_durable_record(self) -> None:
        source = self.write("first.md", "first version\n")
        first = inventory(self.root, self.database, include_records=True)
        second = inventory(self.root, self.database, include_records=True)
        source.write_text("second version\n")
        third = inventory(self.root, self.database, include_records=True)

        self.assertEqual(first["new"], 1)
        self.assertEqual(second["unchanged"], 1)
        self.assertEqual(third["changed"], 1)
        self.assertEqual(len(third["records"]), 1)
        self.assertEqual(
            first["records"][0]["source_id"], third["records"][0]["source_id"]
        )

    def test_missing_source_is_retained_and_can_be_restored(self) -> None:
        source = self.write("first.md", "retained history\n")
        first = inventory(self.root, self.database, include_records=True)
        source.unlink()
        missing = inventory(self.root, self.database, include_records=True)
        source.write_text("retained history\n")
        restored = inventory(self.root, self.database, include_records=True)

        self.assertEqual(missing["missing"], 1)
        self.assertEqual(missing["records"][0]["availability_state"], "missing")
        self.assertEqual(restored["restored"], 1)
        self.assertEqual(restored["records"][0]["availability_state"], "present")
        self.assertEqual(
            restored["records"][0]["content_changed_at"],
            first["records"][0]["content_changed_at"],
        )

    def test_hidden_non_text_and_symlink_sources_are_not_ingested(self) -> None:
        self.write("visible.md", "included\n")
        self.write(".hidden.md", "excluded\n")
        self.write("image.png", "not text\n")
        outside = Path(self.temporary.name) / "outside.md"
        outside.write_text("outside root\n")
        (self.root / "linked.md").symlink_to(outside)
        outside_directory = Path(self.temporary.name) / "outside-directory"
        outside_directory.mkdir()
        (outside_directory / "nested.md").write_text("also outside root\n")
        (self.root / "linked-directory").symlink_to(outside_directory)

        result = inventory(self.root, self.database, include_records=True)
        self.assertEqual(result["new"], 1)
        self.assertEqual(
            [Path(record["source_path"]).name for record in result["records"]],
            ["visible.md"],
        )

    def test_extractor_upgrade_resets_processing_state(self) -> None:
        self.write("first.md", "same content\n")
        inventory(self.root, self.database, extractor_version="extractor-v1")
        with sqlite3.connect(self.database) as db:
            db.execute("UPDATE sources SET processing_state='processed'")
            db.commit()

        result = inventory(
            self.root,
            self.database,
            extractor_version="extractor-v2",
            include_records=True,
        )
        self.assertEqual(result["changed"], 1)
        self.assertEqual(result["records"][0]["processing_state"], "discovered")

    def test_missing_reconciliation_is_scoped_to_the_scanned_root(self) -> None:
        self.write("first.md", "first root\n")
        second_root = Path(self.temporary.name) / "other-sources"
        second_root.mkdir()
        (second_root / "second.md").write_text("second root\n")
        inventory(self.root, self.database)
        inventory(second_root, self.database)

        result = inventory(self.root, self.database)
        self.assertEqual(result["missing"], 0)
        with sqlite3.connect(self.database) as db:
            states = dict(
                db.execute(
                    "SELECT source_path, availability_state FROM sources"
                ).fetchall()
            )
        self.assertEqual(states[str((second_root / "second.md").resolve())], "present")

    def test_unchanged_scan_refreshes_observed_metadata(self) -> None:
        source = self.write("first.md", "same content\n")
        first = inventory(self.root, self.database, include_records=True)
        source.touch()
        second = inventory(self.root, self.database, include_records=True)

        self.assertEqual(second["unchanged"], 1)
        self.assertGreaterEqual(
            second["records"][0]["mtime_ns"], first["records"][0]["mtime_ns"]
        )
        self.assertGreaterEqual(
            second["records"][0]["last_seen_at"],
            first["records"][0]["last_seen_at"],
        )

    def test_failed_scan_rolls_back_all_source_changes(self) -> None:
        self.write("first.md", "one\n")
        self.write("second.md", "two\n")
        real_fingerprint = intake_manifest.file_fingerprint
        calls = 0

        def fail_second(path: Path):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise RuntimeError("simulated unstable source")
            return real_fingerprint(path)

        with mock.patch.object(intake_manifest, "file_fingerprint", fail_second):
            with self.assertRaisesRegex(RuntimeError, "simulated unstable source"):
                inventory(self.root, self.database)

        with sqlite3.connect(self.database) as db:
            count = db.execute("SELECT COUNT(*) FROM sources").fetchone()[0]
        self.assertEqual(count, 0)

    def test_v1_database_is_migrated_without_losing_rows(self) -> None:
        source = self.write("first.md", "migrated\n")
        with sqlite3.connect(self.database) as db:
            db.execute(
                """
                CREATE TABLE sources (
                    source_id TEXT PRIMARY KEY,
                    source_path TEXT NOT NULL UNIQUE,
                    source_type TEXT NOT NULL,
                    content_sha256 TEXT NOT NULL,
                    size_bytes INTEGER NOT NULL,
                    mtime_ns INTEGER NOT NULL,
                    extractor_version TEXT NOT NULL,
                    processing_state TEXT NOT NULL,
                    discovered_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )
            digest, stat = intake_manifest.file_fingerprint(source)
            db.execute(
                """
                INSERT INTO sources VALUES (?, ?, 'md', ?, ?, ?, ?, 'processed', ?, ?)
                """,
                (
                    intake_manifest.stable_id("md", source),
                    str(source.resolve()),
                    digest,
                    stat.st_size,
                    stat.st_mtime_ns,
                    intake_manifest.VERSION,
                    "2026-01-01T00:00:00+00:00",
                    "2026-01-01T00:00:00+00:00",
                ),
            )
            db.commit()

        result = inventory(self.root, self.database, include_records=True)
        self.assertEqual(result["unchanged"], 1)
        self.assertEqual(len(result["records"]), 1)
        self.assertEqual(result["records"][0]["processing_state"], "processed")
        with sqlite3.connect(self.database) as db:
            schema_version = db.execute("PRAGMA user_version").fetchone()[0]
            integrity = db.execute("PRAGMA quick_check").fetchone()[0]
        self.assertEqual(schema_version, intake_manifest.SCHEMA_VERSION)
        self.assertEqual(integrity, "ok")


if __name__ == "__main__":
    unittest.main()
