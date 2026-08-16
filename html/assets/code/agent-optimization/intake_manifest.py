#!/usr/bin/env python3
"""Build a deterministic SQLite inventory for Markdown and text files."""

from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


VERSION = "intake-manifest-v1"
ALLOWED_SUFFIXES = {".md", ".txt"}
SCHEMA = """
CREATE TABLE IF NOT EXISTS sources (
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
);
"""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stable_id(source_type: str, path: Path) -> str:
    identity = f"{source_type}:{path.resolve()}"
    return "src_" + hashlib.sha256(identity.encode()).hexdigest()[:24]


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_files(root: Path) -> list[Path]:
    return [
        path
        for path in sorted(root.rglob("*"))
        if path.is_file()
        and path.suffix.lower() in ALLOWED_SUFFIXES
        and not any(part.startswith(".") for part in path.relative_to(root).parts)
    ]


def inventory(root: Path, database: Path) -> dict[str, int | str]:
    root = root.resolve()
    database = database.resolve()
    if not root.is_dir():
        raise SystemExit(f"source directory does not exist: {root}")
    database.parent.mkdir(parents=True, exist_ok=True)

    counts = {"new": 0, "changed": 0, "unchanged": 0}
    with sqlite3.connect(database) as db:
        db.row_factory = sqlite3.Row
        db.execute(SCHEMA)
        now = utc_now()
        for path in source_files(root):
            absolute = path.resolve()
            source_type = path.suffix.lower().lstrip(".")
            source_id = stable_id(source_type, absolute)
            digest = file_sha256(absolute)
            stat = absolute.stat()
            prior = db.execute(
                "SELECT content_sha256, extractor_version FROM sources WHERE source_id=?",
                (source_id,),
            ).fetchone()

            if prior is None:
                outcome = "new"
            elif (
                prior["content_sha256"] == digest
                and prior["extractor_version"] == VERSION
            ):
                counts["unchanged"] += 1
                continue
            else:
                outcome = "changed"

            counts[outcome] += 1
            db.execute(
                """
                INSERT INTO sources (
                    source_id, source_path, source_type, content_sha256,
                    size_bytes, mtime_ns, extractor_version, processing_state,
                    discovered_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, 'discovered', ?, ?)
                ON CONFLICT(source_id) DO UPDATE SET
                    content_sha256=excluded.content_sha256,
                    size_bytes=excluded.size_bytes,
                    mtime_ns=excluded.mtime_ns,
                    extractor_version=excluded.extractor_version,
                    processing_state='discovered',
                    updated_at=excluded.updated_at
                """,
                (
                    source_id,
                    str(absolute),
                    source_type,
                    digest,
                    stat.st_size,
                    stat.st_mtime_ns,
                    VERSION,
                    now,
                    now,
                ),
            )
        db.commit()
        if db.execute("PRAGMA quick_check").fetchone()[0] != "ok":
            raise SystemExit("manifest integrity check failed")

    return {"schema_version": 1, "extractor_version": VERSION, **counts}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_directory", type=Path)
    parser.add_argument("--db", required=True, type=Path, help="SQLite manifest path")
    args = parser.parse_args()
    print(json.dumps(inventory(args.source_directory, args.db), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
