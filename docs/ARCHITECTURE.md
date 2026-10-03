# Fly Brain Lab — Architecture (Planned)

Status: **DRAFT.** Most components described here remain planned, not
implemented. A narrow exception now exists: neuPrint data access/
authentication, the small deterministic `ORN_DA1 -> DA1_lPN` retrieval,
local raw artifact writing, and provenance/checksum recording are
implemented (see `src/flybrain/`, M1.1 in `docs/ROADMAP.md`). This does not
make the general "Data Access Layer" or "Local Data Store" components
complete — only this one narrow, hard-coded circuit's retrieval path.

## 1. Purpose

This document describes the planned high-level structure of Fly Brain Lab: the
major system boundaries, the expected data/processing pipeline, and how
biological source data is kept separate from computational modelling.

Most of what follows is still a plan, not a report of implemented code.
The current milestone is M1 — Connectome Access (see `ROADMAP.md`), and one
narrow slice of this architecture is now implemented as part of M1.1:
neuPrint authentication, the deterministic `ORN_DA1 -> DA1_lPN` retrieval,
local raw artifact writing, and provenance/checksum recording (see Section
4 below for exactly which components this covers). Everything past that —
the connectivity graph, computational neuron models, simulation, sensory/
motor interfaces, the environment, and plasticity — remains planned and
unimplemented.

Architecture changes must follow the ownership model defined in
`TOOL_ROLES.md`: ChatGPT leads architecture discussion, Claude Code may
propose changes, Sagar approves, Codex independently reviews significant
decisions, and approved decisions are recorded in `DECISION_LOG.md`.

## 2. Core Boundary: Biological Data vs. Computational Model

Per `PROJECT_CHARTER.md` §5, these are never the same thing and must remain
architecturally separate:

- **Biological Source Data** — measured/reconstructed connectome data
  obtained from an authoritative external source (see `DATA_SOURCES.md`).
  Treated as read-only once retrieved; never altered to make a model behave
  a certain way.
- **Computational Model** — code and parameters we write (neuron dynamics,
  plasticity rules, sensory/motor encodings). Every computational model must
  be traceable to an explicit, documented assumption (see
  `ENGINEERING_STANDARDS.md` §7).

## 3. Planned High-Level Pipeline

All stages below are **planned**, not implemented. The sequence follows the
milestones in `ROADMAP.md`.

```
[Biological Source Data]          (external, measured; see DATA_SOURCES.md)
        |
        v
[Data Access Layer]               (PARTIAL — M1.1: neuPrint auth + one hard-coded
                                    ORN_DA1 -> DA1_lPN query implemented; a general
                                    data access layer is still PLANNED)
        |
        v
[Local Data Store]                (PARTIAL — M1.1: raw CSV + checksummed provenance
                                    JSON written to data/raw/da1/; no general local
                                    data store exists yet)
        |
        v
[Connectivity Graph]              (PLANNED — M2: neurons as nodes, connections as edges)
        |
        v
[Computational Neuron Model]      (PLANNED — M4: explicit modelling assumption, not measurement)
        |
        v
[Signal Propagation / Simulation] (PLANNED — M5: activity driven by graph + neuron model)
        |
        v
[Sensory Interface] --> [Circuit] --> [Motor Interface]   (PLANNED — M6)
        |                                     |
        v                                     v
[Artificial Environment] <---- feedback ------+            (PLANNED — M7)
        |
        v
[Plasticity Layer]                (PLANNED — M8: controlled, documented weight change)
        |
        v
[Experiment Harness / Logging]    (PLANNED — cross-cutting; records to EXPERIMENT_LOG.md)
```

Only the two boxes marked PARTIAL above are implemented, and only for the
one hard-coded `ORN_DA1 -> DA1_lPN` circuit — everything else in this
diagram remains **not implemented**. This diagram shows intended
boundaries only; it is not a commitment to a build order beyond what
`ROADMAP.md` already states.

## 4. Component Status

| Component | Status | Notes |
|---|---|---|
| neuPrint data access/authentication | Implemented (narrow) | `src/flybrain/neuprint_client.py`; connects to `male-cns:v1.0` via `neuprint-python`, token from `NEUPRINT_TOKEN` only. Not a general-purpose data access layer. |
| DA1 connectome retrieval | Implemented (narrow) | `src/flybrain/da1_retrieval.py`, `scripts/retrieve_da1.py`; one fixed, deterministic Cypher query for `ORN_DA1 -> DA1_lPN`, top 20 by synapse weight. See `docs/DATA_SOURCES.md`. |
| Local raw artifact writing | Implemented (narrow) | Untouched CSV written under `data/raw/da1/` (git-ignored), refuses to overwrite an existing artifact. |
| Provenance / checksum recording | Implemented (narrow) | SHA-256 checksum, query, dataset, timestamp, row/unique-neuron counts recorded as JSON alongside the CSV. |
| General data access layer | Planned | Only the one narrow DA1 query path above exists; a general retrieval layer for arbitrary circuits is not yet designed |
| General local data store | Planned | Only ad hoc CSV+JSON per retrieval exists; no general storage format decided |
| Connectivity graph representation | Planned | Graph library/approach not yet decided |
| Computational neuron model | Planned | Model family not yet decided — deferred to M4 per roadmap |
| Simulation / propagation engine | Planned | No simulation framework has been chosen |
| Sensory / motor interface | Planned | Encoding/decoding scheme not yet defined |
| Artificial environment | Planned | Not yet designed; expected to start "extremely simple" per roadmap M7 |
| Plasticity layer | Planned | Plasticity rule not yet chosen |
| Experiment harness / logging | Planned | Record format defined in `EXPERIMENT_LOG.md`; no runner implemented |

## 5. Deliberately Deferred Decisions

To avoid choosing technology prematurely, this document intentionally does
**not** decide:

- Which connectome dataset/API client to use (`DATA_SOURCES.md` — NOT YET VERIFIED).
- Graph library / storage format.
- Neuron model family and parameters.
- Simulation engine or numerical framework.
- Sensory encoding and motor decoding schemes.
- Environment implementation.
- Plasticity rule.

Each will be proposed individually, through the architecture ownership
process in `TOOL_ROLES.md`, at the milestone where the roadmap first
requires it.

## 6. Open Architecture Questions

- What is the authoritative access method for the initial connectome
  dataset (API vs. bulk download)?
- What is the minimal local data format sufficient for M1/M2 without
  over-engineering?
- How will "measured" vs. "assumed" data be tagged in code/data structures
  so the biological/model separation (charter §5) is enforced mechanically,
  not just by convention?

## 7. Change Process

Any change to this document that alters a system boundary or commits to a
specific technology must:

1. Be proposed, with rationale.
2. Go through ChatGPT-led architecture discussion.
3. Be approved by Sagar.
4. Be independently reviewed by Codex if the change is significant.
5. Be recorded as a new entry in `DECISION_LOG.md`.
6. Then be reflected here.
