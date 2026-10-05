# Fly Brain Lab — Experiment Log

Status: No experiments have been run yet. This document defines the record
format only (M0 — Project Foundation). Create an entry and complete Phase A
before execution. Complete Phase B/results only after the experiment has
actually executed; do not pre-fill expected results as actual results.

## Purpose

Per `PROJECT_CHARTER.md` §5, every experiment should eventually be
reproducible from source code, configuration, dataset version, random seed
(where applicable), dependencies, experiment documentation, and results.
This log is where that documentation lives.

## Format

Each experiment is recorded in two phases: a pre-run definition, written
and committed *before* the experiment is executed, and a post-run record,
added *after* it has actually run.

```
## E0XX — <experiment title>

### Phase A — Pre-run definition (recorded before execution)

- Date defined:
- Author:
- Related milestone (ROADMAP.md):
- Question / hypothesis:
- Source DATA_SOURCES.md entry (dataset + version used):
- Input artifact path(s) and checksum(s):
- Configuration:
- Random seed(s), where applicable:
- Dependency/environment reference:
- Planned execution command / entry point:
- Expected validation criteria (defined before running):

### Phase B — Post-run record (recorded after execution)

- Date executed:
- Git commit hash used for the run:
- Uncommitted local changes present at run time (yes/no, and what):
- Actual execution command / entry point used:
- Output artifact path(s):
- Observed validation results (compared against the Phase A criteria):
- Results:
- Observations:
- Limitations / deviations from the pre-run definition:
- Conclusion:
  (Must distinguish measured outcome from interpretation; see
  PROJECT_CHARTER.md §5, "Experiments before claims".)
- Follow-up / open questions:
```

Rules:

- Phase A must be written before the experiment is executed. It records
  intent and validation criteria, not results.
- Phase B is only added after the experiment has actually run — never
  pre-filled with expected or assumed results.
- An entry is incomplete (not a finished experiment record) until both
  phases are present.
- "Conclusion" must not claim biological equivalence unless the experiment
  and evidence directly support it (`PROJECT_CHARTER.md` §6).
- If an experiment is repeated with a changed dataset version, seed, or
  configuration, it gets a new entry rather than an edit to the old one.

## Entries

### E001 — M2.1: Selected DA1 Connectivity Graph

#### Phase A — Pre-run definition (recorded before execution)

- Date defined: 2026-10-03
- Author: Sagar (project owner); pre-run definition drafted by Claude Code
  per Sagar's specification.
- Related milestone (ROADMAP.md): M2 — Connectivity Visualisation.
- Question / hypothesis: What connectivity structure exists within the
  selected 20 strongest `ORN_DA1 -> DA1_lPN` `ConnectsTo` edges retrieved
  from `male-cns:v1.0`?
  Planned measurements (not yet computed):
  - node count
  - edge count
  - in-degree per neuron
  - out-degree per neuron
  - total incoming synapse weight per neuron
  - total outgoing synapse weight per neuron
  - convergence of `ORN_DA1` neurons onto `DA1_lPN` neurons
  Scope boundary: this is the selected top-20-strongest-edge subset
  retrieved for M1.1, not the complete DA1 circuit, and the result
  describes only this subset. The neuPrint `synapse_weight` is a
  structural synapse count for the connection; it must not be described
  or interpreted as electrical signal strength. The single planned
  visualisation is one simple static bipartite figure (`ORN_DA1` left,
  `DA1_lPN` right, edges left-to-right) with edge weight labelled as
  synapse count; no other visualisation, simulation, neuron dynamics, or
  plasticity is part of this experiment.
- Source DATA_SOURCES.md entry (dataset + version used): `male-cns:v1.0`
  (Janelia neuPrint) entry in `docs/DATA_SOURCES.md`, retrieved
  2026-10-03T06:24:31.765554+00:00 via `scripts/retrieve_da1.py`.
- Input artifact path(s) and checksum(s):
  `data/raw/da1/orn_da1_to_da1_lpn_20261003T062431Z.csv`;
  SHA-256 `23354c46fec504b4c338c73d1eb3cd8167b4fdca8cfd7a880fbccd9df98fa2fc`.
  Known properties of this artifact (per `docs/DATA_SOURCES.md`): 20
  directed edges, 18 unique `ORN_DA1` source neurons, 5 unique `DA1_lPN`
  target neurons, 23 unique neurons total.
- Configuration: None beyond selecting the single input artifact above; no
  new neuPrint query is issued for this experiment — it operates entirely
  on the already-retrieved CSV.
- Random seed(s), where applicable: Not applicable. All planned
  computations (counts, degree, weight sums, convergence) are
  deterministic given the fixed input artifact.
- Dependency/environment reference: Python 3.12.8 (`.python-version`);
  `networkx==3.7` (directed weighted graph; approved by Sagar for M2.1),
  `matplotlib==3.11.2` (static figure; both approved by Sagar for M2.1
  only, see `docs/DECISION_LOG.md` D005), `pandas==3.0.6`,
  `neuprint-python==0.6.3` (not used by this experiment; no network
  access). All pinned in `pyproject.toml`. See "Amendments" below.
- Planned execution command / entry point: `python scripts/analyze_da1_graph.py`
  (no arguments; reads only the artifact above, verifies its SHA-256 before
  parsing, writes the figure to
  `data/processed/da1/m2_1_selected_connectivity.png`, which is git-ignored).
  See "Amendments" below.
- Expected validation criteria (defined before running): Given the known,
  already-verified properties of the input artifact, a correct
  implementation must reproduce:
  - `node_count == 23`
  - `edge_count == 20`
  - number of nodes with out-degree > 0 (source role) `== 18`
  - number of nodes with in-degree > 0 (target role) `== 5`
  - the source-role and target-role node sets are disjoint (no node acts
    as both an `ORN_DA1` source and a `DA1_lPN` target)
  - sum of out-degree across all nodes `== 20` (equals edge count)
  - sum of in-degree across all nodes `== 20` (equals edge count)
  - sum of "total outgoing synapse weight" across all source nodes equals
    sum of "total incoming synapse weight" across all target nodes equals
    the sum of `synapse_weight` over all 20 edges (a conservation check;
    this total itself is a first-run measurement, not a value predicted
    in advance)
  - the input file's SHA-256 matches the value above, checked before the
    file is parsed
  - exactly 18 nodes typed `ORN_DA1` and exactly 5 typed `DA1_lPN`
    (node type is taken from the retrieval query's type filters, not
    parsed from instance strings)
  - every edge `synapse_weight` is positive (no zero, negative, or missing
    weights)
  If any of these fail, the implementation should be treated as suspect
  first, since the input artifact's checksum above is already fixed and
  verified.
- Amendments (chronology): the fields below were originally recorded on
  2026-10-03 and were amended on 2026-10-04 and 2026-10-05, **after
  implementation planning had begun** (the M2.1 code had been written and
  unit-tested on synthetic fixtures) and **before any execution against the
  real artifact**. No measurement or result influenced these amendments,
  because none existed.
  - Scope boundary: originally stated that visualisation was "a later,
    separate step … out of scope for this experiment's execution". Now
    scopes in exactly one static bipartite figure.
  - Dependency/environment reference: originally "Not yet decided"; no
    graph library approved. Now the pinned versions listed above.
  - Planned execution command / entry point: originally "Not yet
    implemented". Now `python scripts/analyze_da1_graph.py`.
  - Expected validation criteria: the final three bullets (checksum
    verified before parsing; 18 `ORN_DA1` / 5 `DA1_lPN` node types;
    positive weights) were added. The original criteria are
    unchanged.

#### Phase B — Post-run record (recorded after execution)

**NOT EXECUTED.** The analysis code exists and is unit-tested on synthetic
fixtures only. It has not been run against the real input artifact, and no
E001 measurements exist. No results may be recorded here until the script
has been run against the real artifact on Sagar's machine.
