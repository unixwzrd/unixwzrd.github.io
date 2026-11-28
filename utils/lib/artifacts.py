#!/usr/bin/env python3
"""Report old browser diagnostics; delete only explicitly reviewed manifest files."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import stat
import subprocess
import sys
import time
import unicodedata

ROOT = Path(__file__).resolve().parents[2]
BROWSER_ROOTS = ("output/playwright", ".playwright-cli")
MARKERS = (".keep", ".active")


class ArtifactError(ValueError):
    pass


def path_key(value):
    # Conservatively protect case/Unicode aliases of tracked files on APFS.
    # On case-sensitive hosts this may retain an extra diagnostic, never delete
    # an extra file. Do not rely on sys.platform to guess filesystem behavior.
    return unicodedata.normalize("NFC", value).casefold()


def tracked_files(root):
    actual = subprocess.check_output(["git", "-C", str(root), "rev-parse", "--show-toplevel"], text=True).strip()
    if Path(actual).resolve() != root:
        raise ArtifactError("Cleanup requires the exact repository root.")
    data = subprocess.check_output(["git", "-C", str(root), "ls-files", "-z"])
    return set(path_key(os.fsdecode(p)) for p in data.split(b"\0") if p)


def checked_path(root, relative, tracked):
    if not isinstance(relative, str):
        raise ArtifactError("Manifest paths must be strings.")
    parts = PurePosixPath(relative).parts
    if not parts or PurePosixPath(relative).is_absolute() or ".." in parts or str(PurePosixPath(relative)) != relative:
        raise ArtifactError(f"Unsafe path: {relative}")
    if not any(relative.startswith(prefix + "/") for prefix in BROWSER_ROOTS):
        raise ArtifactError(f"Outside browser artifact locations: {relative}")
    if path_key(relative) in tracked:
        raise ArtifactError(f"Tracked file protected: {relative}")
    current = root
    for part in parts:
        current = current / part
        if current.is_symlink():
            raise ArtifactError(f"Symlink protected: {relative}")
        if current.is_dir() and any((current / marker).exists() or (current / marker).is_symlink() for marker in MARKERS):
            raise ArtifactError(f"Pinned or active run protected: {relative}")
    if parts[-1] in (*MARKERS, ".run.json"):
        raise ArtifactError(f"Run metadata protected: {relative}")
    if not stat.S_ISREG(current.lstat().st_mode):
        raise ArtifactError(f"Not a regular file: {relative}")
    return current


def fingerprint(path):
    # Refuse final-component symlinks even if substituted after traversal.
    with os.fdopen(os.open(path, os.O_RDONLY | os.O_NOFOLLOW), "rb") as handle:
        before = os.fstat(handle.fileno())
        digest = hashlib.sha256()
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
        after = os.fstat(handle.fileno())
    if (before.st_size, before.st_mtime_ns, before.st_ino) != (after.st_size, after.st_mtime_ns, after.st_ino):
        raise ArtifactError(f"Artifact changed while reading: {path}")
    return {"size": before.st_size, "mtime_ns": before.st_mtime_ns, "sha256": digest.hexdigest()}


def remove_verified(root, relative, expected):
    # Resolve every directory through held FDs, never through a pathname after
    # validation. Renaming a parent and replacing it with a symlink must not
    # redirect unlink to an unrelated file outside the reviewed run.
    descriptors = [os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)]
    try:
        parts = PurePosixPath(relative).parts
        for part in parts[:-1]:
            descriptors.append(os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=descriptors[-1]))
        for descriptor in descriptors:
            for marker in MARKERS:
                try:
                    os.stat(marker, dir_fd=descriptor, follow_symlinks=False)
                except FileNotFoundError:
                    continue
                raise ArtifactError(f"Pinned or active ancestor protected: {relative}")
        parent = descriptors[-1]
        with os.fdopen(os.open(parts[-1], os.O_RDONLY | os.O_NOFOLLOW, dir_fd=parent), "rb") as handle:
            before = os.fstat(handle.fileno())
            digest = hashlib.sha256()
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
            after = os.fstat(handle.fileno())
            current = os.stat(parts[-1], dir_fd=parent, follow_symlinks=False)
            actual = {"size": after.st_size, "mtime_ns": after.st_mtime_ns, "sha256": digest.hexdigest()}
            if actual != expected or (before.st_ino, before.st_mtime_ns, before.st_size) != (after.st_ino, after.st_mtime_ns, after.st_size) or (current.st_dev, current.st_ino) != (after.st_dev, after.st_ino):
                raise ArtifactError(f"Changed during cleanup: {relative}")
            os.unlink(parts[-1], dir_fd=parent)
    finally:
        for descriptor in reversed(descriptors):
            os.close(descriptor)


def report(root, days=30, with_hashes=False, now=None):
    root = Path(root).resolve()
    if type(days) is not int or days < 1:
        raise ArtifactError("Age must be at least one day.")
    now = time.time() if now is None else now
    tracked = tracked_files(root)
    files = []
    protected = 0
    for prefix in BROWSER_ROOTS:
        start = root / prefix
        if not start.exists():
            continue
        # os.walk does not itself reject a symlink passed as its top-level root.
        if any(p.is_symlink() for p in [start, *start.parents] if p != root.parent):
            protected += 1
            continue
        for directory, dirs, names in os.walk(start, followlinks=False):
            directory = Path(directory)
            if any((directory / marker).exists() or (directory / marker).is_symlink() for marker in MARKERS):
                dirs[:] = []
                protected += 1
                continue
            dirs[:] = sorted(d for d in dirs if not (directory / d).is_symlink())
            for name in sorted(names):
                path = directory / name
                relative = path.relative_to(root).as_posix()
                try:
                    path = checked_path(root, relative, tracked)
                except ArtifactError:
                    protected += 1
                    continue
                info = path.stat()
                if now - info.st_mtime <= days * 86400:
                    continue
                entry = {"path": relative, "size": info.st_size, "mtime_ns": info.st_mtime_ns}
                if with_hashes:
                    entry.update(fingerprint(path))
                files.append(entry)
    return {"version": 1, "root": str(root), "generated_at": datetime.fromtimestamp(now, timezone.utc).isoformat(),
            "older_than_days": days, "protected": protected, "files": sorted(files, key=lambda f: f["path"])}


def apply_manifest(root, manifest):
    root = Path(root).resolve()
    if manifest.get("version") != 1 or manifest.get("root") != str(root):
        raise ArtifactError("Manifest version/root does not match this repository.")
    days = manifest.get("older_than_days")
    if type(days) is not int or days < 1 or not isinstance(manifest.get("files"), list):
        raise ArtifactError("Invalid manifest age or file list.")
    tracked = tracked_files(root)
    validated = []
    seen = set()
    # Validate the entire selection before deleting anything.
    for entry in manifest["files"]:
        if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
            raise ArtifactError("Invalid manifest entry.")
        relative = entry["path"]
        if relative in seen:
            raise ArtifactError(f"Duplicate selection: {relative}")
        seen.add(relative)
        path = checked_path(root, relative, tracked)
        expected = {key: entry.get(key) for key in ("size", "mtime_ns", "sha256")}
        if fingerprint(path) != expected or time.time() - path.stat().st_mtime <= days * 86400:
            raise ArtifactError(f"Artifact changed or is too recent: {relative}; regenerate the report.")
        validated.append((relative, expected))
    removed = 0
    for relative, expected in validated:
        checked_path(root, relative, tracked)
        remove_verified(root, relative, expected)
        removed += 1
        print(f"Removed: {relative}")
    return removed


def main():
    parser = argparse.ArgumentParser(description=__doc__, epilog="Report-only by default. --apply permanently removes only listed files; no directories are removed.")
    parser.add_argument("--older-than-days", type=int, default=30)
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--manifest", type=Path, help="Write a NEW review manifest; never overwrite one")
    action.add_argument("--apply", type=Path, help="Apply a reviewed manifest (explicit permanent deletion)")
    args = parser.parse_args()
    try:
        if args.apply:
            manifest = json.loads(args.apply.read_text())
            if not isinstance(manifest, dict):
                raise ArtifactError("Manifest must be an object.")
            count = apply_manifest(ROOT, manifest)
            print(f"Removed {count} reviewed artifact files. No directories were removed.")
        else:
            manifest = report(ROOT, args.older_than_days, with_hashes=bool(args.manifest))
            total = sum(entry["size"] for entry in manifest["files"])
            print(f"Browser artifacts older than {args.older_than_days} days: {len(manifest['files'])} files, {total / 1024**2:.1f} MiB. Report only; nothing deleted.")
            for entry in manifest["files"][:20]:
                print(f"  {entry['path']} ({entry['size']} bytes)")
            print(f"Protected entries/runs: {manifest['protected']}. Legacy output requires review; ignored does not mean disposable.")
            if args.manifest:
                with args.manifest.open("x") as handle:
                    json.dump(manifest, handle, indent=2)
                    handle.write("\n")
                print(f"Review {args.manifest}; remove entries you want to retain. --apply is permanent deletion, never a CI default.")
        return 0
    except (ArtifactError, OSError, subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        print(f"Artifact cleanup refused: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

