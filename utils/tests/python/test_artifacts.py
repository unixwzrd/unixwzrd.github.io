"""All deletion scenarios use disposable repositories, never real diagnostics."""
import copy
import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from utils.lib import artifacts


class ArtifactTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="artifact-fixture-")
        self.root = Path(self.temp.name).resolve()
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)

    def tearDown(self):
        self.temp.cleanup()

    def artifact(self, name="output/playwright/run/screen.png", age=31):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"fixture evidence")
        stamp = time.time() - age * 86400
        os.utime(path, (stamp, stamp))
        return path

    def manifest(self):
        return artifacts.report(self.root, with_hashes=True)

    def test_report_is_non_mutating_and_filters_recent_files(self):
        old = self.artifact()
        recent = self.artifact(".playwright-cli/recent.log", age=1)
        before = {p: p.read_bytes() for p in (old, recent)}
        manifest = self.manifest()
        self.assertEqual(["output/playwright/run/screen.png"], [f["path"] for f in manifest["files"]])
        self.assertEqual(before, {p: p.read_bytes() for p in before})

    def test_exact_age_boundary_is_not_selected(self):
        path = self.artifact()
        now = path.stat().st_mtime + 30 * 86400
        self.assertEqual([], artifacts.report(self.root, now=now)["files"])

    def test_only_reviewed_manifest_files_are_removed(self):
        selected = self.artifact()
        retained = self.artifact(".playwright-cli/other.log")
        manifest = self.manifest()
        manifest["files"] = [entry for entry in manifest["files"] if entry["path"].endswith("screen.png")]
        self.assertEqual(1, artifacts.apply_manifest(self.root, manifest))
        self.assertFalse(selected.exists())
        self.assertTrue(retained.exists())
        self.assertTrue(selected.parent.exists(), "Never recursively delete run directories")

    def test_active_and_pinned_runs_are_protected(self):
        for marker in (".active", ".keep"):
            path = self.artifact(f"output/playwright/{marker[1:]}/image.png")
            (path.parent / marker).write_text("protected")
        self.assertEqual([], self.manifest()["files"])

    def test_pin_added_after_review_prevents_deletion(self):
        path = self.artifact()
        manifest = self.manifest()
        (path.parent / ".keep").touch()
        with self.assertRaises(artifacts.ArtifactError):
            artifacts.apply_manifest(self.root, manifest)
        self.assertTrue(path.exists())

    def test_symlink_file_and_directory_are_never_followed(self):
        outside = self.artifact("private/evidence.png")
        target = self.root / "output/playwright"
        target.mkdir(parents=True)
        (target / "file.png").symlink_to(outside)
        (target / "directory").symlink_to(outside.parent, target_is_directory=True)
        self.assertEqual([], self.manifest()["files"])
        self.assertTrue(outside.exists())

    def test_symlinked_allowed_root_is_not_traversed(self):
        outside = self.artifact("private/evidence.png")
        (self.root / "output").mkdir()
        (self.root / "output/playwright").symlink_to(outside.parent, target_is_directory=True)
        self.assertEqual([], self.manifest()["files"])

    def test_tracked_files_protected_before_and_after_manifest(self):
        path = self.artifact()
        manifest = self.manifest()
        subprocess.run(["git", "-C", str(self.root), "add", "--", str(path)], check=True)
        self.assertEqual([], self.manifest()["files"])
        with self.assertRaises(artifacts.ArtifactError):
            artifacts.apply_manifest(self.root, manifest)

    def test_tracked_case_aliases_are_protected_on_case_insensitive_filesystems(self):
        path = self.artifact()
        subprocess.run(["git", "-C", str(self.root), "add", "--", str(path)], check=True)
        subprocess.run(["git", "-C", str(self.root), "mv", "--", "output", "intermediate-output"], check=True)
        subprocess.run(["git", "-C", str(self.root), "mv", "--", "intermediate-output", "Output"], check=True)
        self.assertEqual([], self.manifest()["files"])
        self.assertEqual(artifacts.path_key("Output/playwright/Screen.PNG"), artifacts.path_key("output/playwright/screen.png"))

    def test_changed_file_rejects_whole_selection_before_deletion(self):
        first = self.artifact()
        other = self.artifact("output/playwright/z/other.png")
        manifest = self.manifest()
        other.write_bytes(b"new evidence")
        with self.assertRaises(artifacts.ArtifactError):
            artifacts.apply_manifest(self.root, manifest)
        self.assertTrue(first.exists())
        self.assertTrue(other.exists())

    def test_path_escape_absolute_path_and_unrelated_output_are_rejected(self):
        self.artifact()
        base = self.manifest()
        for relative in ("../outside.png", "/tmp/outside.png", "output/playwright/../../secret", "utils/output/report.json", "html/assets/image.png"):
            manifest = copy.deepcopy(base)
            manifest["files"][0]["path"] = relative
            with self.subTest(relative=relative), self.assertRaises(artifacts.ArtifactError):
                artifacts.apply_manifest(self.root, manifest)

    def test_duplicate_missing_and_wrong_root_manifests_are_rejected(self):
        path = self.artifact()
        base = self.manifest()
        manifest = copy.deepcopy(base)
        manifest["files"] *= 2
        with self.assertRaises(artifacts.ArtifactError):
            artifacts.apply_manifest(self.root, manifest)
        manifest = copy.deepcopy(base)
        manifest["root"] += "/other"
        with self.assertRaises(artifacts.ArtifactError):
            artifacts.apply_manifest(self.root, manifest)
        path.unlink()
        with self.assertRaises(OSError):
            artifacts.apply_manifest(self.root, base)

    def test_marker_and_run_metadata_files_are_not_candidates(self):
        self.artifact("output/playwright/run/.run.json")
        self.assertEqual([], self.manifest()["files"])

    def test_invalid_ages_fail_closed(self):
        for age in (0, -1, True, "30"):
            with self.assertRaises(artifacts.ArtifactError):
                artifacts.report(self.root, age)

    def test_ancestor_swapped_after_verification_cannot_redirect_unlink(self):
        path = self.artifact()
        expected = artifacts.fingerprint(path)
        private = self.artifact("private/screen.png")
        moved = self.root / "moved-approved-run"
        original_stat = os.stat
        swapped = False
        def swap_after_final_stat(name, **kwargs):
            nonlocal swapped
            result = original_stat(name, **kwargs)
            if name == "screen.png" and "dir_fd" in kwargs and not swapped:
                path.parent.rename(moved)
                path.parent.symlink_to(private.parent, target_is_directory=True)
                swapped = True
            return result
        with mock.patch.object(artifacts.os, "stat", side_effect=swap_after_final_stat):
            artifacts.remove_verified(self.root, "output/playwright/run/screen.png", expected)
        self.assertTrue(swapped)
        self.assertEqual(b"fixture evidence", private.read_bytes())
        self.assertFalse((moved / "screen.png").exists())


if __name__ == "__main__":
    unittest.main()

