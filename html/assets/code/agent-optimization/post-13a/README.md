# Agent Isolation Manifest Preflight

This model-free teaching package checks an invented two-agent declaration for obvious ownership collisions before anyone provisions or starts the environment. It uses Python 3.10 or newer and the standard library.

It does not inspect users, processes, launchd, files, ports, credentials, channels, synchronization, SSH, or a model server. `MANIFEST READY FOR ISOLATED TEST` means only that the declaration is internally consistent enough to begin a separately reviewed live test.

Run the ready manifest:

```bash
python3 -B isolation_preflight.py fixtures/ready.json
```

Exercise the collision fixtures:

```bash
python3 -B isolation_preflight.py fixtures/shared-root.json || test $? -eq 1
python3 -B isolation_preflight.py fixtures/shared-port.json || test $? -eq 1
python3 -B isolation_preflight.py fixtures/shared-vault-writers.json || test $? -eq 1
```

Run the fixed walkthrough and unit tests:

```bash
python3 -B run_lab.py
python3 -B -m unittest -v test_isolation_preflight.py
```

The ready fixture declares two different execution users, process-manager domains, root sets, credential canaries, channel canaries, and same-host listener ports. Its shared writable test Vault has one owner and one writer. An immutable shared corpus has no writer. Both clients declare attributable use of one remote inference dependency plus planned contention and failure canaries.

Collection fields are set-like and reject duplicate entries. Shared stores require at least two participating agents, non-shared stores allow no more than one participant, and the contention and endpoint-failure canaries must have different identifiers. These are declaration checks only; none of the listed tests is executed by this package.

The manifest contains symbolic names, not deployable paths or secrets. Replace none of those examples with private data in a publication artifact. A real collector and acceptance procedure belong behind a separate privilege, privacy, and approval boundary.
