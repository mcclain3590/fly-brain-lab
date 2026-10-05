# Fly Brain Lab — Decision Log

Lightweight Architecture Decision Record (ADR) log. Per `TOOL_ROLES.md` §9,
significant decisions — architectural, methodological, or process — are
recorded here once approved, following the architecture ownership model in
`TOOL_ROLES.md`.

## Format

Each entry follows this template:

```
## D0XX — <short title>

- Status: Proposed | Accepted | Superseded by D0YY
- Date: YYYY-MM-DD
- Approved by: who approved this decision
- Context: why this decision was needed
- Decision: what was decided
- Evidence / source: the existing project documentation or discussion
  that established this decision
- Consequences: what this implies or constrains going forward
```

Entries are never deleted. A changed decision is recorded as a new entry
that supersedes an earlier one; the earlier entry's status is updated to
reflect the supersession.

---

## D001 — GitHub is the single source of truth

- Status: Accepted
- Date: 2026-09-25
- Approved by: Sagar
- Context: The project uses multiple AI tools (ChatGPT, Claude Code, Codex,
  Cursor) and a personal notebook (Obsidian). Without one authoritative
  record, decisions could conflict or be lost between tools.
- Decision: GitHub holds all authoritative project state — source code,
  architecture, roadmap, engineering standards, dataset provenance,
  experiment definitions, decisions, tests, and dependency configuration.
  Information existing only in an AI conversation or Obsidian is not an
  authoritative decision until written into GitHub.
- Evidence / source: `PROJECT_CHARTER.md` §9 and `TOOL_ROLES.md` §2,
  established in the project foundation commit (`4ef98de`).
- Consequences: Every significant decision, including ones made in AI
  conversations, must be promoted into the repository (e.g. into this log)
  to count as decided.

## D002 — Start with small connectome subsets rather than whole-system simulation

- Status: Accepted
- Date: 2026-09-25
- Approved by: Sagar
- Context: A whole-brain or whole-connectome simulation is not
  understandable or verifiable as a first step, and risks scaling before
  understanding.
- Decision: The project will initially access and work with small subsets
  of the connectome (an initial target of approximately 10–20 neurons, per
  `ROADMAP.md` M1) rather than downloading or simulating the entire
  dataset.
- Evidence / source: `PROJECT_CHARTER.md` §4–§5 and `ROADMAP.md` M1,
  established in the project foundation commit (`4ef98de`).
- Consequences: Early milestones (M1–M5) are scoped around small,
  inspectable circuits. Scaling to larger systems (`ROADMAP.md` M10) is
  deferred until earlier milestones are stable, tested, and understood.

## D003 — Separate biological measurements from computational assumptions

- Status: Accepted
- Date: 2026-09-25
- Approved by: Sagar
- Context: Connectome data is biological measurement/reconstruction;
  anything built on top of it (neuron dynamics, plasticity rules,
  encodings) is a modelling choice introduced by the project. Conflating
  the two would undermine the project's scientific honesty goal.
- Decision: Biological data and computational models must never be
  described as the same thing. Every computational model or assumption
  must be documented as such, separately from the biological data it is
  derived from (`PROJECT_CHARTER.md` §5–§6, `ENGINEERING_STANDARDS.md` §7).
- Evidence / source: `PROJECT_CHARTER.md` §5–§6 and `TOOL_ROLES.md` §11,
  established in the project foundation commit (`4ef98de`).
- Consequences: `ARCHITECTURE.md` keeps biological data and
  computational-model components as distinct boundaries. Claims about
  biological behaviour require documented assumptions and experimental
  evidence (`EXPERIMENT_LOG.md`), not just interesting output.

## D004 — Architecture ownership model clarified during M0

- Status: Accepted
- Date: 2026-09-25
- Approved by: Sagar
- Context: `TOOL_ROLES.md` defined tool responsibilities but left ambiguous
  who originates architecture proposals versus who approves them, which
  could let architecture drift without a clear decision-maker.
- Decision: Sagar is the final decision-maker for architecture. ChatGPT
  leads architecture and research-design discussions. Claude Code may
  propose architecture and engineering improvements but must not
  independently redefine approved architecture, and implements
  architecture once it is approved. Codex independently reviews important
  implementation and architectural decisions. GitHub records the resulting
  authoritative decisions (this log).
- Evidence / source: project owner instruction clarifying the architecture
  ownership model during M0 continuation, reflected in the corresponding
  `TOOL_ROLES.md` update.
- Consequences: `TOOL_ROLES.md` updated accordingly. Future architecture
  changes (e.g. to `ARCHITECTURE.md`) must follow this chain: propose →
  ChatGPT-led discussion → Sagar approval → Codex review of significant
  work → recorded here.

## D005 — NetworkX and Matplotlib for M2.1 static graph analysis and visualisation

- Status: Accepted (scope limited to M2.1; see Decision)
- Date: 2026-10-04 (proposed); accepted 2026-10-05
- Approved by: Sagar. NetworkX was specified in the M2.1 implementation
  instruction; NetworkX `3.7` and Matplotlib `3.11.2` were then both
  explicitly approved on 2026-10-05.
- Context: `ARCHITECTURE.md` §5 deferred the graph library choice until the
  roadmap first required it. M2.1 (experiment E001) is that point: it needs
  a directed weighted graph of the selected 20 `ORN_DA1 -> DA1_lPN` edges
  plus one static figure.
- Decision: Use `networkx==3.7` (`DiGraph`) and `matplotlib==3.11.2`, both
  pinned in `pyproject.toml`, **for M2.1 static graph analysis and
  visualisation only**. They are used in `src/flybrain/da1_graph.py`,
  `src/flybrain/da1_graph_plot.py` and `scripts/analyze_da1_graph.py`, which
  handle only the selected DA1 edge table. This is not a general graph
  framework.
- Evidence / source: Sagar's M2.1 instruction and 2026-10-05 approval;
  `docs/EXPERIMENT_LOG.md` E001 Phase A.
- Consequences: Two new runtime dependencies. This does **not** select
  either library for simulation (M5), larger circuits, or whole-connectome
  work; the graph representation for those remains undecided and will need
  its own decision.
