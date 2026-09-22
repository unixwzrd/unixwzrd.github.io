# Release Evidence Ledger

This model-free teaching package validates an invented release-evidence packet. It demonstrates that implementation capability, exact-artifact acceptance, and release publication are separate records. Exact artifact identity includes the version, expected release tag, source commit, archive digest, and manifest digest.

The clean fixture contains observable prerelease metadata and archive evidence while installation and lifecycle gates remain incomplete. A successful validation therefore says exactly:

```text
EVIDENCE PACKET READY FOR REVIEW
```

It never infers `RELEASE READY`, `APPROVED`, or `PUBLISHED`.

## Requirements

- Python 3.10 or newer
- Python standard library only

## Run the clean packet

```bash
python3 -B release_evidence.py fixtures/review-ready.json
```

## Run the failure cases

```bash
python3 -B release_evidence.py fixtures/missing-gate.json
python3 -B release_evidence.py fixtures/identity-mismatch.json
python3 -B release_evidence.py fixtures/manifest-mismatch.json
python3 -B release_evidence.py fixtures/stale-evidence.json
python3 -B release_evidence.py fixtures/unsupported-approval.json
```

Each command above returns status 1 with a bounded error code. Rejected private-looking values are never echoed.

## Run acceptance and unit tests

```bash
python3 -B run_lab.py
python3 -B -m unittest -v test_release_evidence.py
```

## Boundary

The package reads only the JSON file supplied on the command line. It performs no build, installation, network access, Git action, CI query, signing, upload, approval, or publication. Its publication state is supplied evidence, not a state discovered or inferred by the program.
