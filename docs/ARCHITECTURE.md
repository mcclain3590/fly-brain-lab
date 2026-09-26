# Fly Brain Lab — Architecture (Planned)

Status: **DRAFT — structural document only. No component described here is implemented yet.**

## 1. Purpose

This document describes the planned high-level structure of Fly Brain Lab: the
major system boundaries, the expected data/processing pipeline, and how
biological source data is kept separate from computational modelling.

It does not describe existing software. Everything below is a plan, not a
report of implemented code, consistent with the current milestone (see
`ROADMAP.md`, M0 — Project Foundation).

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
[Biological Source Data]          (external, measured; PLANNED — see DATA_SOURCES.md)
        |
        v
[Data Access Layer]               (PLANNED — M1: retrieval from authoritative source)
        |
        v
[Local Data Store]                (PLANNED — M1: small, verified subset)
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

Every box above is **not implemented**. This diagram shows intended
boundaries only; it is not a commitment to a build order beyond what
`ROADMAP.md` already states.

## 4. Component Status

| Component | Status | Notes |
|---|---|---|
| Data access layer | Planned | Target dataset/API not yet chosen or verified — see `DATA_SOURCES.md` |
| Local data store | Planned | Storage format not yet decided |
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
