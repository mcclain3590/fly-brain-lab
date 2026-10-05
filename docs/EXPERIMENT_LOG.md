# Fly Brain Lab — Experiment Log

Status: One experiment has been executed: E001 (selected DA1 connectivity
graph, M2.1), run on 2026-10-05 against the checksummed real artifact; its
Phase B record is below. Create an entry and complete Phase A before
executing any further experiment. Complete Phase B/results only after the
experiment has actually executed; do not pre-fill expected results as actual
results.

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

- Provenance of this record: E001 was executed on **Sagar's Mac** against
  the authoritative real artifact. It was **not** executed in Claude Code's
  sandbox, which does not contain the git-ignored raw artifact. Claude Code
  did not run the experiment and has not seen the raw CSV or the generated
  figure; the results below were recorded by Claude Code from execution
  evidence supplied by Sagar and have not been independently reproduced by
  Claude Code. This record was written on 2026-10-05. The execution
  provenance fields below (date, commit, command, working-tree state) were
  confirmed by Sagar after the initial record and are as reported by Sagar.
- Date executed: 2026-10-05.
- Git commit hash used for the run:
  `1481bee2c2ffdaf761ba70ff1794cd4d817a28ae` (the M2.1 implementation
  commit on `feature/m2-1-connectivity-graph`).
- Uncommitted local changes present at run time (yes/no, and what): No
  tracked or uncommitted source changes were reported during the
  experiment. The implementation commit was checked out immediately before
  validation and execution. The execution itself generated the git-ignored
  output `data/processed/da1/m2_1_selected_connectivity.png`; git-ignored
  files (the raw input artifact and, after execution, that PNG) were
  therefore present on the filesystem.
- Execution environment (as reported): Python 3.12.8, networkx 3.7, pandas
  3.0.6, matplotlib 3.11.2. This matches the Phase A dependency reference.
- Actual execution command / entry point used:
  `python scripts/analyze_da1_graph.py`, run on Sagar's Mac (the Phase A
  entry point).
- Input artifact: `data/raw/da1/orn_da1_to_da1_lpn_20261003T062431Z.csv`.
  SHA-256 `23354c46fec504b4c338c73d1eb3cd8167b4fdca8cfd7a880fbccd9df98fa2fc`
  was reported verified before analysis, matching Phase A.
- Output artifact path(s): `data/processed/da1/m2_1_selected_connectivity.png`
  (git-ignored; not committed). Sagar visually inspected the figure and
  approved it as sufficiently clear for M2.1.
- Observed validation results (compared against the Phase A criteria): the
  input SHA-256 was verified before analysis, and all nine analysis
  validation checks passed (the nine lines printed under VALIDATION).
  - Input SHA-256 verified before analysis (separate from the nine graph
    validation checks below): PASS
  - `node_count`: expected 23, got 23
  - `edge_count`: expected 20, got 20
  - `ORN_DA1_node_count`: expected 18, got 18
  - `DA1_lPN_node_count`: expected 5, got 5
  - `source_target_disjoint`: 0 nodes have both incoming and outgoing edges
  - `sum_in_degree`: expected 20, got 20
  - `sum_out_degree`: expected 20, got 20
  - `positive_synapse_weights`: 0 missing or non-positive edges
  - `weight_conservation`: incoming 984, outgoing 984, edge total 984
  The Phase A criteria "nodes with out-degree > 0 == 18" and "nodes with
  in-degree > 0 == 5" are not separate script checks; they are covered by
  the node-type-count and disjointness checks above, and are consistent
  with the reported degree data (derived by Claude Code by arithmetic from
  the reported figures: 16 sources with out-degree 1 and 2 with out-degree
  2 give 18 source nodes and 20 edges; the 5 DA1_lPN nodes have 7 + 5 + 3 +
  3 + 2 = 20 incoming edges).
- Results:
  - Global: 23 nodes; 20 edges; total structural synapse weight 984. (The
    total of 984 is a first-run measurement; Phase A did not predict it.)
  - `DA1_lPN` convergence in this selected sample (body ID / instance;
    distinct selected `ORN_DA1` sources; total incoming structural
    synapse weight):
    - 11780 / `DA1_lPN_R`: 7 sources; 365
    - 12122 / `DA1_lPN_R`: 5 sources; 239
    - 11996 / `DA1_lPN_R`: 3 sources; 144
    - 11816 / `DA1_lPN_R`: 3 sources; 142
    - 13064 / `DA1_lPN_R`: 2 sources; 94
  - Additional observed graph structure: `ORN_DA1` 152946 has out-degree 2
    and total outgoing weight 101; `ORN_DA1` 118367 has out-degree 2 and
    total outgoing weight 94; all other selected `ORN_DA1` nodes have
    out-degree 1.
  - Evidence basis: Sagar confirms that the complete experiment console
    output, including the per-node table, was supplied after execution and
    used to verify the summary recorded here. The per-node table is not
    duplicated in this log (the log template does not require it); the
    complete console output remains with Sagar. Individual edge weights are
    not listed here: they are represented in the generated figure and
    originate from the authoritative input artifact, and no information
    beyond the supplied evidence is added.
- Observations (measured; scope limited to the selected edges):
  - Among the five `DA1_lPN` nodes in the selected sample, body ID 11780
    has both the most distinct selected `ORN_DA1` sources (7) and the
    largest total incoming structural synapse weight (365). The remaining
    four, in order of incoming weight, are 12122 (5 sources; 239), 11996
    (3; 144), 11816 (3; 142) and 13064 (2; 94).
  - The five incoming totals sum to 984, equal to the total edge weight.
  - Only two selected `ORN_DA1` neurons (152946 and 118367) have edges to
    two `DA1_lPN` targets; every other selected `ORN_DA1` neuron has one.
- Limitations / deviations from the pre-run definition:
  - Scope: these results describe only the selected top-20 strongest
    `ORN_DA1 -> DA1_lPN` structural connections retrieved in M1.1. They are
    not the complete DA1 circuit. Any `ORN_DA1 -> DA1_lPN` edges outside
    that selection were not retrieved or analysed, so the source counts and
    weights above describe selected edges only and may not equal any
    `DA1_lPN` neuron's complete `ORN_DA1` input.
  - `synapse_weight` is the neuPrint structural synapse count for a
    connection (measured/reconstructed structure). It is not electrical or
    physiological signal strength and not functional connection strength.
  - Node type (`ORN_DA1` / `DA1_lPN`) comes from the retrieval query's type
    filters, not from parsing instance strings.
  - Deviations from Phase A: none reported in the evidence supplied. The
    run followed the Phase A definition as amended before execution (see
    Phase A, "Amendments").
  - The figure's clarity was judged visually by Sagar; this is a human
    judgment, not an automated check.
- Conclusion:
  - Measured outcome: on the real artifact, all nine analysis validation
    checks passed and the input SHA-256 was verified before analysis,
    reproducing the Phase A expected counts (23 nodes, 20 edges, 18 `ORN_DA1`
    and 5 `DA1_lPN` nodes) and the weight-conservation check. The selected
    graph has total structural synapse weight 984, with `DA1_lPN`
    convergence as listed under Results.
  - Interpretation (narrow): within the selected top-20 strongest
    `ORN_DA1 -> DA1_lPN` structural connections, `DA1_lPN` body ID 11780
    shows the greatest convergence: 7 distinct selected `ORN_DA1` sources
    representing 365 synapses.
  - Not claimed: that 11780 is the most important DA1 neuron; that it
    receives the strongest physiological or electrical signal; that these
    20 edges represent the complete DA1 circuit; that synapse count is
    equivalent to functional connection strength; or any biological
    equivalence (`PROJECT_CHARTER.md` §6). The visualisation and
    measurements describe only the selected top-20 structural connections.
- Follow-up / open questions:
  - Any extension beyond the selected 20 edges would be a new experiment
    with its own Phase A (per the rules above); none is proposed here.
