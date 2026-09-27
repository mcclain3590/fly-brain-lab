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

**M0 — Project Foundation, in progress** (see `docs/ROADMAP.md`). No source
code has been implemented yet. This milestone establishes the repository,
governance documentation, and Python project scaffolding.

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
docs/            Governance, architecture and research documentation
src/flybrain/    Python package source (planned; not yet created)
data/raw/        Raw retrieved dataset artifacts (planned; git-ignored except placeholders)
data/processed/  Derived/processed data artifacts (planned; git-ignored except placeholders)
pyproject.toml   Minimal Python project configuration
```

## Requirements

- Supported Python series (per `pyproject.toml`): **`>=3.12,<3.13`**
- Validated development interpreter (pinned in `.python-version`):
  **Python 3.12.8**. This is the specific patch version local development
  has been verified against; it does not imply other 3.12.x patch versions
  are unsupported.

## Environment Setup

No runtime dependencies are declared yet — M0 does not include connectome
access or simulation code (see `docs/ENGINEERING_STANDARDS.md`). A minimal
local environment can be created with:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

Dependencies (e.g. for connectome access) will be added in a later milestone
once the corresponding architecture is proposed and approved.

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
  and pipeline (nothing described there is implemented yet)
- [`docs/ENGINEERING_STANDARDS.md`](docs/ENGINEERING_STANDARDS.md) —
  code quality, testing, reproducibility and assumption-documentation
  standards
- [`docs/DATA_SOURCES.md`](docs/DATA_SOURCES.md) — connectome dataset
  provenance template (not yet filled in)
- [`docs/DECISION_LOG.md`](docs/DECISION_LOG.md) — architecture decision
  record
- [`docs/EXPERIMENT_LOG.md`](docs/EXPERIMENT_LOG.md) — experiment record
  template (no experiments have been run yet)
