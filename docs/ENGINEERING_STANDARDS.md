# Fly Brain Lab — Engineering Standards

Status: Living document. Establishes principles and structure for M0.
Specific tool choices (test runner, formatter, linter, etc.) are not fixed
here — they are to be proposed and approved through the architecture
ownership model in `TOOL_ROLES.md` before adoption.

## 1. Purpose

Defines the engineering principles Fly Brain Lab code and documentation
should follow, so implementation quality, reproducibility and scientific
honesty (per `PROJECT_CHARTER.md`) stay consistent regardless of which tool
or person writes the code.

## 2. Code Quality Principles

- Prefer the simplest implementation that answers the current question
  (`PROJECT_CHARTER.md` §12).
- Avoid speculative generality: do not build for a milestone that hasn't
  started.
- Favor small, readable functions and modules over clever ones.
- Use type hints on public functions once Python code begins.
- No dead code and no commented-out code left in the repository.
- Naming should make the biological-vs-computational distinction visible
  in code (e.g. a name that clearly reads as measured data vs. a name that
  clearly reads as a modelling assumption), so the charter's separation
  rule (§5) is enforced in code, not only in docs.

## 3. Testing Expectations

- Non-trivial logic (anything beyond a trivial data pass-through) should
  have automated tests before being considered complete.
- Tests must be deterministic: fixed seeds wherever randomness is involved.
- Tests operate on small, checked-in or clearly-sourced fixture data —
  never on the full connectome dataset.
- The specific test framework/tooling is not fixed by this document and
  should be proposed through the normal architecture process before
  adoption.

## 4. Documentation Requirements

- Every module should state its purpose briefly: what it does and, where
  relevant, what it deliberately does not do.
- Every computational modelling assumption must be documented at the point
  it is introduced (see §7 below), not left implicit in code.
- User-facing docs (`README.md`, `ARCHITECTURE.md`, this file) must stay in
  sync with what is actually implemented; "planned" vs. "implemented"
  status must be kept accurate.

## 5. Reproducibility Requirements

Per `PROJECT_CHARTER.md` §5, an experiment should eventually be
reproducible from:

- source code (versioned in GitHub),
- configuration (versioned, not hardcoded inline where it varies by run),
- dataset version (recorded per `DATA_SOURCES.md`),
- random seed, where applicable,
- dependencies (pinned once a dependency manifest exists),
- experiment documentation (recorded per `EXPERIMENT_LOG.md`),
- results.

No experiment result should be reported without these being recorded.

## 6. Configuration & Secrets Rules

Per `TOOL_ROLES.md` §10:

- Never commit API tokens, passwords, private keys, credentials, or other
  local secrets.
- Secrets must be supplied via environment variables or files excluded
  from version control.
- Configuration that affects experiment outcomes (parameters, dataset
  version, seeds) must be explicit and recorded, not buried in code
  defaults that silently change.

## 7. Scientific Assumption Documentation

Per `PROJECT_CHARTER.md` §5–§6:

- Any place code introduces a computational assumption not directly
  present in the biological data (a neuron model, a plasticity rule, a
  sensory encoding, etc.) must document that assumption where it is
  introduced (`ARCHITECTURE.md` or a dedicated assumptions note).
- Code and docs must distinguish **measured biological data** from
  **computational assumptions introduced by us**, per `TOOL_ROLES.md` §11.
- Interesting behaviour is not evidence of biological equivalence on its
  own; claims require a recorded experiment (`EXPERIMENT_LOG.md`).

## 8. Simplicity Before Optimisation

- Correctness and clarity come before performance.
- Do not optimise, parallelise, or scale code before there is a working,
  understood, small-scale version (`PROJECT_CHARTER.md` §5, "Understand
  before scaling").
- Scaling up (larger circuits, more neurons) is itself an experiment, not
  a default next step (`ROADMAP.md` M10).

## 9. Status of This Document

This document defines standards, not a completed checklist. It should be
revisited as implementation begins and specific tool/library choices are
approved through the architecture ownership process.

## 10. Proportional Process for Tooling Choices

Not every choice requires the full architecture/ADR process. Routine,
low-risk developer tooling — for example a code formatter, a linter, an
ordinary test runner, or local development convenience tooling — may be
proposed and approved through a lightweight project-owner decision,
without ChatGPT-led architecture discussion, Codex review, or a
`DECISION_LOG.md` entry.

The full architecture decision/review process (`TOOL_ROLES.md`,
`ARCHITECTURE.md` §7) remains required whenever a choice materially
affects:

- biological data interpretation,
- scientific assumptions,
- reproducibility,
- persistent data formats/interfaces,
- simulation behaviour,
- major dependencies,
- architecture/system boundaries,
- project structure.

This keeps process proportional to a small research project: heavyweight
review is reserved for decisions that could compromise scientific honesty
or reproducibility, not applied uniformly to every tool choice.
