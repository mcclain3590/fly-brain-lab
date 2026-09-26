# Fly Brain Lab — Tool Roles

## Purpose

Fly Brain Lab uses multiple AI and development tools.

Each tool has a defined responsibility to prevent duplicated work,
conflicting decisions and uncontrolled architectural changes.

GitHub remains the single source of truth.

---

# 1. Sagar — Project Owner / Engineer

Responsibilities:

- understand the system being built,
- approve major project direction,
- learn the engineering and neuroscience concepts,
- run and inspect experiments,
- challenge assumptions,
- approve final architecture decisions,
- make final project decisions.

Rule:

No important code should remain in the project if the project owner
cannot explain its purpose at an appropriate level.

---

# 2. GitHub — Single Source of Truth

GitHub owns authoritative project state.

Store in GitHub:

- source code,
- architecture,
- roadmap,
- engineering standards,
- dataset provenance,
- experiment definitions,
- decisions,
- tests,
- dependency configuration,
- reproducibility information.

If information exists only in an AI conversation or Obsidian,
it is not an authoritative engineering decision.

---

# 3. ChatGPT — Project Lead / Technical Teacher

Primary responsibilities:

- guide milestones,
- teach concepts,
- challenge assumptions,
- control scope,
- explain neuroscience and AI concepts,
- help design experiments,
- lead architecture and research-design discussions,
- connect implementation work to the research question.

ChatGPT should prefer understanding before implementation.

ChatGPT does not become a second source of truth.

Important decisions from conversations must be written into GitHub.

---

# 4. Claude Code — Primary Implementation Engineer

Primary responsibilities:

- propose architecture and engineering improvements for approval,
- implement approved architecture,
- create production-quality Python modules,
- refactor code,
- work across repository files,
- implement tests,
- investigate implementation problems.

Claude Code should work from existing repository documentation.

Claude Code must not independently redefine:

- project scope,
- scientific claims,
- architecture,
- dataset assumptions,
- experiment objectives.

Proposed architecture or engineering changes must go through ChatGPT-led
architecture discussion and be approved by Sagar before implementation.
Major changes should be proposed before implementation.

---

# 5. Codex — Independent Engineering Reviewer

Primary responsibilities:

- review implementations,
- identify bugs,
- challenge assumptions,
- independently review important architectural decisions,
- review tests,
- identify missing edge cases,
- suggest simpler implementations,
- independently verify important engineering work.

Codex should not merely agree with Claude Code.

Its purpose is independent technical criticism.

---

# 6. Cursor — Engineering Workbench

Primary responsibilities:

- inspect code,
- make focused edits,
- run code,
- debug,
- navigate the repository,
- understand implementation details.

Cursor is the primary interactive coding workspace.

Large architectural decisions should not originate solely from
Cursor autocomplete or agent suggestions.

---

# 7. Obsidian — Research & Learning Notebook

Obsidian stores:

- neuroscience notes,
- learning notes,
- research-paper notes,
- hypotheses,
- questions,
- explanations,
- experiment ideas,
- personal understanding.

Obsidian is NOT the authoritative engineering source.

When an idea becomes an engineering or scientific decision,
it must be promoted into the GitHub repository.

---

# 8. Agent Workflow

Normal implementation flow:

Research / Question
        ↓
ChatGPT discussion
        ↓
Decision documented in GitHub
        ↓
Claude Code implementation
        ↓
Tests
        ↓
Codex independent review
        ↓
Fixes if required
        ↓
Sagar runs and understands result
        ↓
Commit to GitHub
        ↓
Experiment documented

Not every tiny change requires every tool.

Use the smallest workflow appropriate to the risk.

Routine, low-risk developer tooling choices — for example a formatter, a
linter, an ordinary test runner, or local development convenience tooling
— do not require the full architecture/ADR process. They may be proposed
and approved through a lightweight project-owner decision.

The full process (ChatGPT-led discussion, Sagar approval, Codex review,
and a `DECISION_LOG.md` entry) remains required when a choice materially
affects biological data interpretation, scientific assumptions,
reproducibility, persistent data formats/interfaces, simulation behaviour,
major dependencies, or architecture/system boundaries (see
`ENGINEERING_STANDARDS.md` §10).

---

# 9. Conflict Resolution

If AI agents disagree:

1. Do not choose based on confidence or writing style.
2. Identify the actual technical disagreement.
3. Check documentation, source data or experimental evidence.
4. Run a test where possible.
5. Record significant decisions in `DECISION_LOG.md`.

Evidence outranks agent opinion.

---

# 10. Security

Never commit:

- API tokens,
- passwords,
- private keys,
- credentials,
- local secrets.

Secrets must use environment variables or ignored local files.

---

# 11. Scientific Integrity

AI-generated explanations are not scientific evidence.

Claims about biological behaviour must ultimately be supported by:

- authoritative datasets,
- scientific literature,
- documented assumptions,
- reproducible experiments.

The project must distinguish between:

**measured biological data**

and

**computational assumptions introduced by us.**

---

# 12. Core Rule

AI tools accelerate the project.

They do not replace understanding.

---

# 13. Workspace Verification

Before an AI agent reviews or modifies repository state, it must verify
the repository/worktree it is operating on (repository root, branch and
HEAD). It must not assume that two clones of the same GitHub repository
share working-tree state.
