#!/usr/bin/env python3
"""Offline regression entry point. Never builds, installs, stages or restarts."""
import argparse
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site", type=Path, help="Existing production build, not an active preview")
    args = parser.parse_args()
    env = os.environ.copy()
    if args.site:
        site = args.site.resolve()
        if not (site / "index.html").is_file():
            parser.error("--site must contain an existing rendered index.html")
        for key in ("READER_SITE", "SECKIT_PRODUCTION_SITE", "ATTRIBUTION_SITE", "JEKYLL_DESTINATION"):
            env[key] = str(site)
    commands = [["bundle", "check"]]
    commands += [["bundle", "exec", "ruby", str(path)] for path in sorted((ROOT / "utils/tests/ruby").glob("test_*.rb"))]
    commands += [[sys.executable, "-m", "unittest", "discover", "-s", "utils/tests/python", "-p", "test_*.py"]]
    if args.site:
        commands += [["bundle", "exec", "ruby", str(ROOT / path)] for path in (
            "utils/bin/checks/check_permalinks.rb", "utils/bin/checks/check_tag_taxonomy.rb",
            "utils/bin/checks/verify_short_url_redirects.rb", "utils/bin/checks/verify_project_permalink_redirects.rb")]
        commands += [["bundle", "exec", "ruby", "utils/bin/backfill_short_url_front_matter.rb", "--check"]]
        commands += [["bundle", "exec", "htmlproofer", str(site), "--disable-external", "--allow-hash-href", "--check-internal-hash", "--allow-missing-href"]]
    for command in commands:
        print("Running:", " ".join(command), flush=True)
        result = subprocess.run(command, cwd=ROOT, env=env)
        if result.returncode:
            return result.returncode
    print("All deterministic checks passed; no manual service/email/network diagnostics executed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

