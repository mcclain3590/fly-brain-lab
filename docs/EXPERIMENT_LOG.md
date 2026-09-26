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

_No experiments have been run yet._
