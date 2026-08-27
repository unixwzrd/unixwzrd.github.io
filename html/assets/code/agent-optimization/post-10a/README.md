# Fail-Closed Inference Benchmark Comparator

This small lab compares invented benchmark bundles without loading a model, contacting a service, or reading private evidence. It is a teaching implementation, not an export from MLXForge.

Run the bounded walkthrough:

```bash
python run_lab.py
```

Run the tests:

```bash
python -m unittest -v test_lab.py
```

Compare either candidate directly:

```bash
python benchmark_compare.py fixtures/baseline.json fixtures/candidate-optimization.json
python benchmark_compare.py fixtures/baseline.json fixtures/candidate-ineligible.json
```

The second command exits with status 2 because a warm baseline and cold candidate are not comparable. That is the intended result.

The schema is closed. It contains fingerprints, execution conditions, correctness state, and numeric observations, but no prompt, generated output, hostname, user, address, token, credential, or private path. A normalized output hash only proves equality under the chosen normalization; it does not prove answer quality.

Generated projections live only in a temporary directory during `run_lab.py` and are removed before the runner reports success. The eight package files are the complete end state.
