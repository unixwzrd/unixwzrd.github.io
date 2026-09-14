# LLM-Ops Component Triage Teaching Package

This model-free package turns invented, sanitized capture fixtures into deterministic component-restart review packets. It uses Python 3.10 or newer and the standard library. It does not invoke `llmops`, start a subprocess, use the network, discover a filesystem, retrieve a secret, or execute a lifecycle operation.

Run the complete example:

```bash
python3 -B scripts/triage_packet.py fixtures/complete.json --as-of 2030-01-02T03:09:05Z --format markdown
```

Compare the incomplete and stale cases:

```bash
python3 -B scripts/triage_packet.py fixtures/unobserved.json --as-of 2030-01-02T03:09:05Z --format markdown
python3 -B scripts/triage_packet.py fixtures/stale.json --as-of 2030-01-02T03:09:05Z --format json
```

Run acceptance and unit checks:

```bash
python3 -B run_lab.py
python3 -B -m unittest -v test_triage_packet.py
```

The fixtures are teaching records, not current operational evidence. A live collector and any executor are deliberately out of scope.
