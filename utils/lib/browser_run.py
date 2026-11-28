#!/usr/bin/env python3
"""Run an existing browser audit with owned session and retained run evidence."""
import argparse
from datetime import datetime, timezone
import ipaddress
import json
import os
from pathlib import Path
import secrets
import shutil
import subprocess
import sys
import tempfile
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[2]
SUITES = ("local-reader", "reader-experience", "secrets-kit-product", "short-link-attribution")


def local_url(value):
    url = urlparse(value)
    if url.scheme != "http" or not url.hostname or url.username or url.password:
        raise ValueError("Use a local HTTP preview URL without credentials.")
    host = url.hostname
    if host == "localhost" or host.endswith(".local"):
        return value
    try:
        address = ipaddress.ip_address(host)
        private = address.is_loopback or any(address in network for network in (
            ipaddress.ip_network("10.0.0.0/8"), ipaddress.ip_network("172.16.0.0/12"), ipaddress.ip_network("192.168.0.0/16")) if address.version == network.version)
        if private:
            return value
    except ValueError:
        pass
    raise ValueError("Browser audits cannot target production or public hosts.")


def run_audit(suite, url, cli, browser="webkit", root=ROOT):
    local_url(url)
    root = Path(root)
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + secrets.token_hex(3)
    directory = root / "output/playwright" / f"{suite}-{run_id}"
    directory.mkdir(parents=True)
    (directory / ".active").write_text(f"{os.getpid()}\n")
    session = "dts-" + suite + "-" + secrets.token_hex(3)
    env = os.environ.copy()
    env["npm_config_offline"] = "true"
    prefix = [str(cli), "--session", session]
    status = "failed"
    opened = False
    try:
        source = (root / "utils/tests/browser" / f"check_{suite.replace('-', '_')}_browser.js").read_text()
        source = source.replace("output/playwright/", directory.as_posix() + "/")
        # Playwright run-code intentionally has no filesystem/process globals.
        # Keep lifecycle bookkeeping here, outside its sandbox.
        wrapped = f'''async (page) => {{
          const url = {json.dumps(url)};
          const base = new URL(url).origin;
          await page.context().route("**/*", route => new URL(route.request().url()).origin === base ? route.fallback() : route.abort());
          await page.goto(url);
          return ({source})(page);
        }}'''
        with tempfile.TemporaryDirectory(prefix="site-browser-audit-") as temp:
            script = Path(temp) / "audit.js"
            script.write_text(wrapped)
            opened = True
            result = subprocess.run(prefix + ["open", "about:blank", "--browser", browser], cwd=root, env=env, capture_output=True, text=True)
            if result.returncode:
                raise RuntimeError(result.stdout + result.stderr)
            result = subprocess.run(prefix + ["run-code", "--filename", str(script)], cwd=root, env=env, capture_output=True, text=True)
            (directory / "audit.log").write_text(result.stdout + result.stderr)
            print(result.stdout, end="")
            print(result.stderr, end="", file=sys.stderr)
            if result.returncode or "### Error" in result.stdout:
                raise RuntimeError(f"Browser audit failed; see {directory / 'audit.log'}")
        status = "passed"
    finally:
        if opened:
            closed = subprocess.run(prefix + ["close"], cwd=root, env=env, capture_output=True, text=True)
            if closed.returncode:
                status = "failed"
                print(f"Could not close owned browser session {session}: {closed.stderr}", file=sys.stderr)
        (directory / ".run.json").write_text(json.dumps({"suite": suite, "status": status, "finished_at": datetime.now(timezone.utc).isoformat()}, indent=2))
        if status == "failed":
            (directory / ".keep").write_text("Failed evidence: review before removing this pin.\n")
        (directory / ".active").unlink()
        print(f"Browser evidence ({status}): {directory}")
    if status != "passed":
        raise RuntimeError("Browser lifecycle incomplete; retained pinned evidence.")
    return directory


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("suite", choices=SUITES)
    parser.add_argument("--url", required=True, help="Existing local HTTP page; attribution requires redirects.json")
    parser.add_argument("--cli", default=shutil.which("playwright-cli"), help="Installed Playwright CLI or skill wrapper; never installs packages")
    parser.add_argument("--browser", default="webkit", choices=("webkit", "chromium", "firefox"))
    args = parser.parse_args()
    try:
        if not args.cli:
            raise ValueError("No Playwright CLI found. Supply --cli with an existing installation or skill wrapper.")
        run_audit(args.suite, args.url, args.cli, args.browser)
        return 0
    except (OSError, ValueError, RuntimeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

