#!/usr/bin/env python3
"""Maintain a deterministic SQLite inventory for Markdown and text files."""

from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


VERSION = "intake-manifest-v2"
SCHEMA_VERSION = 2
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
    availability_state TEXT NOT NULL,
    discovered_at TEXT NOT NULL,
    content_changed_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    last_seen_at TEXT NOT NULL
);
"""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stable_id(source_type: str, path: Path) -> str:
    """Return an identity stable for one source type and canonical path."""
    identity = f"{source_type}:{path.resolve()}"
    return "src_" + hashlib.sha256(identity.encode()).hexdigest()[:24]


def file_fingerprint(path: Path) -> tuple[str, Any]:
    """Hash a file and refuse a result if it changed during the read."""
    before = path.stat()
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    after = path.stat()
    if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
        raise RuntimeError(f"source changed while being fingerprinted: {path}")
    return digest.hexdigest(), after


def source_files(root: Path) -> list[Path]:
    """Return allowlisted regular files without following file symlinks."""
    return [
        path
        for path in sorted(root.rglob("*"))
        if path.is_file()
        and not path.is_symlink()
        and is_below(path, root)
        and path.suffix.lower() in ALLOWED_SUFFIXES
        and not any(part.startswith(".") for part in path.relative_to(root).parts)
    ]


def is_below(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root)
    except ValueError:
        return False
    return True


def ensure_schema(db: sqlite3.Connection) -> None:
    """Create v2 or migrate the original teaching schema without data loss."""
    db.execute(SCHEMA)
    columns = {
        str(row[1]) for row in db.execute("PRAGMA table_info(sources)").fetchall()
    }
    additions = {
        "availability_state": "TEXT NOT NULL DEFAULT 'present'",
        "content_changed_at": "TEXT NOT NULL DEFAULT ''",
        "last_seen_at": "TEXT NOT NULL DEFAULT ''",
    }
    for name, definition in additions.items():
        if name not in columns:
            db.execute(f"ALTER TABLE sources ADD COLUMN {name} {definition}")
    db.execute(
        "UPDATE sources SET content_changed_at=updated_at WHERE content_changed_at=''"
    )
    db.execute("UPDATE sources SET last_seen_at=updated_at WHERE last_seen_at=''")
    db.execute(f"PRAGMA user_version={SCHEMA_VERSION}")
    db.commit()


def manifest_records(db: sqlite3.Connection, root: Path) -> list[dict[str, Any]]:
    rows = db.execute(
        """
        SELECT source_id, source_path, source_type, content_sha256,
               size_bytes, mtime_ns, extractor_version, processing_state,
               availability_state, discovered_at, content_changed_at,
               updated_at, last_seen_at
        FROM sources
        ORDER BY source_path
        """
    ).fetchall()
    return [dict(row) for row in rows if is_below(Path(row["source_path"]), root)]


def inventory(
    root: Path,
    database: Path,
    *,
    extractor_version: str = VERSION,
    include_records: bool = False,
) -> dict[str, Any]:
    root = root.resolve()
    database = database.resolve()
    if not root.is_dir():
        raise SystemExit(f"source directory does not exist: {root}")
    database.parent.mkdir(parents=True, exist_ok=True)

    counts = {
        "new": 0,
        "changed": 0,
        "unchanged": 0,
        "restored": 0,
        "missing": 0,
    }
    with sqlite3.connect(database) as db:
        db.row_factory = sqlite3.Row
        ensure_schema(db)
        db.execute("BEGIN IMMEDIATE")
        now = utc_now()
        seen: set[str] = set()

        try:
            for path in source_files(root):
                absolute = path.resolve()
                source_type = path.suffix.lower().lstrip(".")
                source_id = stable_id(source_type, absolute)
                digest, stat = file_fingerprint(absolute)
                seen.add(source_id)
                prior = db.execute(
                    """
                    SELECT content_sha256, extractor_version, availability_state
                    FROM sources WHERE source_id=?
                    """,
                    (source_id,),
                ).fetchone()

                if prior is None:
                    counts["new"] += 1
                    db.execute(
                        """
                        INSERT INTO sources (
                            source_id, source_path, source_type, content_sha256,
                            size_bytes, mtime_ns, extractor_version,
                            processing_state, availability_state, discovered_at,
                            content_changed_at, updated_at, last_seen_at
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, 'discovered', 'present',
                                  ?, ?, ?, ?)
                        """,
                        (
                            source_id,
                            str(absolute),
                            source_type,
                            digest,
                            stat.st_size,
                            stat.st_mtime_ns,
                            extractor_version,
                            now,
                            now,
                            now,
                            now,
                        ),
                    )
                    continue

                same_content = prior["content_sha256"] == digest
                same_version = prior["extractor_version"] == extractor_version
                was_missing = prior["availability_state"] == "missing"

                if same_content and same_version and not was_missing:
                    counts["unchanged"] += 1
                    db.execute(
                        """
                        UPDATE sources
                        SET source_path=?, size_bytes=?, mtime_ns=?,
                            availability_state='present', last_seen_at=?
                        WHERE source_id=?
                        """,
                        (
                            str(absolute),
                            stat.st_size,
                            stat.st_mtime_ns,
                            now,
                            source_id,
                        ),
                    )
                    continue

                if same_content and same_version:
                    counts["restored"] += 1
                    db.execute(
                        """
                        UPDATE sources
                        SET source_path=?, source_type=?, size_bytes=?, mtime_ns=?,
                            processing_state='discovered',
                            availability_state='present', updated_at=?, last_seen_at=?
                        WHERE source_id=?
                        """,
                        (
                            str(absolute),
                            source_type,
                            stat.st_size,
                            stat.st_mtime_ns,
                            now,
                            now,
                            source_id,
                        ),
                    )
                    continue

                counts["changed"] += 1
                db.execute(
                    """
                    UPDATE sources
                    SET source_path=?, source_type=?, content_sha256=?,
                        size_bytes=?, mtime_ns=?, extractor_version=?,
                        processing_state='discovered', availability_state='present',
                        content_changed_at=?, updated_at=?, last_seen_at=?
                    WHERE source_id=?
                    """,
                    (
                        str(absolute),
                        source_type,
                        digest,
                        stat.st_size,
                        stat.st_mtime_ns,
                        extractor_version,
                        now,
                        now,
                        now,
                        source_id,
                    ),
                )

            prior_rows = db.execute(
                "SELECT source_id, source_path, availability_state FROM sources"
            ).fetchall()
            for row in prior_rows:
                if (
                    row["source_id"] not in seen
                    and row["availability_state"] != "missing"
                    and is_below(Path(row["source_path"]), root)
                ):
                    counts["missing"] += 1
                    db.execute(
                        """
                        UPDATE sources
                        SET availability_state='missing', updated_at=?
                        WHERE source_id=?
                        """,
                        (now, row["source_id"]),
                    )

            check = db.execute("PRAGMA quick_check").fetchone()[0]
            if check != "ok":
                raise RuntimeError(f"manifest integrity check failed: {check}")
            db.commit()
        except Exception:
            db.rollback()
            raise

        result: dict[str, Any] = {
            "schema_version": SCHEMA_VERSION,
            "extractor_version": extractor_version,
            **counts,
        }
        if include_records:
            result["records"] = manifest_records(db, root)
        return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_directory", type=Path)
    parser.add_argument("--db", required=True, type=Path, help="SQLite manifest path")
    parser.add_argument(
        "--records",
        action="store_true",
        help="include ordered records for this source root in the JSON result",
    )
    args = parser.parse_args()
    print(
        json.dumps(
            inventory(args.source_directory, args.db, include_records=args.records),
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
