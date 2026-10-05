# Fly Brain Lab

Experimental software-engineering and computational-neuroscience project for
exploring biological neural circuits derived from the Drosophila connectome.

## Purpose

Fly Brain Lab starts with small, understandable subsets of real connectome
data and progressively investigates biological connectivity, neural circuit
structure, computational neuron dynamics, signal propagation, sensory-to-motor
pathways, synaptic plasticity, learning and memory, and emergent behaviour.
The project prioritises understanding, reproducibility and scientific honesty
over impressive demonstrations (see `docs/PROJECT_CHARTER.md`).

## Research Question

Can computational neural systems constructed from measured Drosophila
connectome topology exhibit meaningful signal propagation, adaptation,
learning and behaviour when coupled to artificial sensory inputs and
environments? This is investigated experimentally; no outcome is assumed in
advance (`docs/PROJECT_CHARTER.md` §3).

## Current Status

**M0 — Project Foundation: COMPLETE.** **M1 — Connectome Access: IN
PROGRESS** (see `docs/ROADMAP.md`). The first narrow slice of M1 (M1.1) is
implemented and has been run live: a deterministic retrieval of the
`ORN_DA1 -> DA1_lPN` circuit from the `male-cns:v1.0` dataset via neuPrint
(see `src/flybrain/`, `docs/DATA_SOURCES.md`). This is one hard-coded
circuit, not a general connectome access layer — most of M1 and all later
milestones remain planned.

## Scientific Scope & Caution

The Drosophila connectome used here is **structural, measured biological
data** — it is not itself a living brain, and it does not by itself define
complete neural dynamics. Any computational neuron or circuit model built
from this data is a modelling assumption introduced by this project, and
must be documented and distinguished from the underlying biological
measurement. This project does not claim to recreate a living fly,
resurrect an individual animal, recover its memories, reproduce
consciousness, or prove that simulated behaviour is biologically equivalent
(see `docs/PROJECT_CHARTER.md` §5–§6).

## Repository Structure

```
docs/              Governance, architecture and research documentation
src/flybrain/      Python package: neuPrint connection, DA1 retrieval, and
                   selected-DA1 graph analysis/figure (M2.1)
scripts/           Runnable entry points (retrieve_da1.py, analyze_da1_graph.py)
tests/             Unit tests (no network access or credentials required)
data/raw/da1/      Raw retrieval artifacts for the DA1 circuit (git-ignored;
                   never committed — see docs/DATA_SOURCES.md for provenance)
data/processed/    Derived outputs, e.g. the M2.1 figure (git-ignored)
pyproject.toml     Python project configuration and dependencies
```

## Requirements

- Supported Python series (per `pyproject.toml`): **`>=3.12,<3.13`**
- Validated development interpreter (pinned in `.python-version`):
  **Python 3.12.8**. This is the specific patch version local development
  has been verified against; it does not imply other 3.12.x patch versions
  are unsupported.
- Runtime dependencies (pinned in `pyproject.toml`, matching the validated
  retrieval environment): `neuprint-python==0.6.3`, `pandas==3.0.6`,
  plus, for M2.1 graph analysis, `networkx==3.7` and `matplotlib==3.11.2`
  (see `docs/DECISION_LOG.md` D005).
- Test dependency: `pytest` (version not yet pinned/validated against a
  specific release — see `docs/ENGINEERING_STANDARDS.md` §10 on routine
  tooling choices).

## Environment Setup

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e ".[test]"
```

Run the test suite (no network access or neuPrint credentials required —
see `tests/`):

```bash
pytest
```

To run the actual DA1 connectome retrieval, you need a neuPrint auth token.
**Never commit, print, or hard-code the token.** Export it as an
environment variable for the one command that needs it, then run the
script:

```bash
export NEUPRINT_TOKEN="<your token>"
python scripts/retrieve_da1.py
```

This saves the raw CSV and a provenance JSON (checksum, query, timestamp,
row/unique-neuron counts) under `data/raw/da1/`, which is git-ignored — the
retrieved data itself is never committed, only its provenance record (see
`docs/DATA_SOURCES.md`).

## Selected DA1 Graph Analysis (E001 / M2.1)

Once the raw artifact named in `docs/EXPERIMENT_LOG.md` (E001) is present
under `data/raw/da1/`, analyse it — no token or network access needed:

```bash
python scripts/analyze_da1_graph.py
```

**Status:** the M2.1 implementation exists and its unit tests (synthetic
fixtures only) pass. Real E001 execution against the retrieved artifact has
**not yet occurred**, so no E001 results exist.

The script verifies the input's SHA-256 before parsing, runs the E001
validation checks, prints global / per-node / `DA1_lPN` convergence
metrics, and saves one static figure to
`data/processed/da1/m2_1_selected_connectivity.png` (git-ignored). It covers
only the selected top-20 strongest `ORN_DA1 -> DA1_lPN` edges, not the
complete DA1 circuit, and `synapse_weight` is a structural synapse count,
not electrical signal strength.

## Governance & Documentation

GitHub is this project's single source of truth (`docs/PROJECT_CHARTER.md`
§9). Start here:

- [`docs/PROJECT_CHARTER.md`](docs/PROJECT_CHARTER.md) — mission, scientific
  boundaries, and success criteria
- [`docs/ROADMAP.md`](docs/ROADMAP.md) — milestones M0–M10
- [`docs/TOOL_ROLES.md`](docs/TOOL_ROLES.md) — responsibilities of each
  person/tool contributing to the project, and the architecture ownership
  model
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — planned system boundaries
  and pipeline, with current implementation status per component
- [`docs/ENGINEERING_STANDARDS.md`](docs/ENGINEERING_STANDARDS.md) —
  code quality, testing, reproducibility and assumption-documentation
  standards
- [`docs/DATA_SOURCES.md`](docs/DATA_SOURCES.md) — connectome dataset
  provenance template and the current entry for `male-cns:v1.0`
- [`docs/DECISION_LOG.md`](docs/DECISION_LOG.md) — architecture decision
  record
- [`docs/EXPERIMENT_LOG.md`](docs/EXPERIMENT_LOG.md) — experiment record
  template (no experiments have been run yet)
