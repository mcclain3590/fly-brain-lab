# Fly Brain Lab — Data Sources

Status: **PARTIALLY VERIFIED.** M1 — Connectome Access is now IN PROGRESS
(see `ROADMAP.md`). Dataset/endpoint access has been verified live by the
project owner; the first checksummed retrieval artifact via
`scripts/retrieve_da1.py` has not been produced yet. No field below may be
filled with a guessed, assumed, or remembered value — fields not yet
independently verified are marked PENDING VERIFICATION.

## Purpose

Per `PROJECT_CHARTER.md` §4, dataset provenance, versions, access methods
and citations must be documented here before, or as part of, retrieving any
biological data.

## How to Use This Document

1. Do not fill in a field unless it has been directly verified against the
   authoritative source (the source's own site, API, or publication) at the
   time of use.
2. If a value is unknown or unverified, leave it as `NOT YET VERIFIED` — do
   not guess, estimate, or carry over a remembered value.
3. Add a new dated entry for each dataset (or dataset version) used; do not
   overwrite a previous entry's history.
4. Record the retrieval so a future reader (or the project owner) can
   independently re-obtain the same data.

## Provenance Template

Copy this block for each dataset/version used. Beyond identifying the
dataset itself, this template also records enough detail about the
retrieval process to reproduce that exact retrieval later.

### Dataset Entry: [name — NOT YET VERIFIED]

| Field | Value |
|---|---|
| Source organisation | NOT YET VERIFIED |
| Dataset name | NOT YET VERIFIED |
| Dataset version / release | NOT YET VERIFIED |
| URL | NOT YET VERIFIED |
| Access method (API / bulk download / client library) | NOT YET VERIFIED |
| Licence | NOT YET VERIFIED |
| Citation (paper / DOI) | NOT YET VERIFIED |
| Retrieval date | NOT YET VERIFIED |
| Retrieved by | NOT YET VERIFIED |
| Subset retrieved (e.g. neuron count/IDs) | NOT YET VERIFIED |
| Exact query / request or retrieval parameters | NOT YET VERIFIED |
| Retrieval script / command or code entry point | NOT YET VERIFIED |
| Filtering criteria applied | NOT YET VERIFIED |
| Retrieved neuron/record IDs (exact list, where practical) | NOT YET VERIFIED |
| Local raw artifact path | NOT YET VERIFIED |
| Checksum / hash of retrieved artifact | NOT YET VERIFIED |
| Schema / field snapshot or notes | NOT YET VERIFIED |
| Transformations applied, if any | NOT YET VERIFIED |
| Notes / caveats | NOT YET VERIFIED |

## Current Entries

### Dataset Entry: male-cns:v1.0 (Janelia neuPrint)

| Field | Value |
|---|---|
| Source organisation | Janelia (neuPrint) |
| Dataset name | male-cns |
| Dataset version / release | v1.0 — as reported by a live neuPrint connection test |
| URL | https://neuprint.janelia.org |
| Access method | `neuprint-python` client library, authenticated via the `NEUPRINT_TOKEN` environment variable |
| Licence | PENDING VERIFICATION |
| Citation (paper / DOI) | PENDING VERIFICATION |
| Retrieval date | PENDING — to be recorded from the provenance JSON produced by `scripts/retrieve_da1.py` once run with network access and a valid token |
| Retrieved by | Sagar (project owner), via `scripts/retrieve_da1.py` |
| Subset retrieved (e.g. neuron count/IDs) | `ORN_DA1 -> DA1_lPN` `ConnectsTo` edges, top 20 by synapse weight (see selection rule below) |
| Exact query / request or retrieval parameters | See Cypher query below |
| Retrieval script / command or code entry point | `scripts/retrieve_da1.py` (`src/flybrain/neuprint_client.py`, `src/flybrain/da1_retrieval.py`) |
| Filtering criteria applied | `a.type = 'ORN_DA1' AND b.type = 'DA1_lPN'`, ordered by `synapse_weight DESC, source_body_id ASC, target_body_id ASC`, `LIMIT 20` |
| Retrieved neuron/record IDs (exact list, where practical) | PENDING — to be recorded from the checksummed CSV produced by `scripts/retrieve_da1.py` |
| Local raw artifact path | PENDING — will be written under `data/raw/da1/` (git-ignored; see `.gitignore`) |
| Checksum / hash of retrieved artifact | PENDING — recorded in the provenance JSON saved alongside the CSV |
| Schema / field snapshot or notes | `source_body_id`, `source_instance`, `target_body_id`, `target_instance`, `synapse_weight` (as returned by the Cypher query) |
| Transformations applied, if any | None — the raw query result is saved untouched |
| Notes / caveats | An exploratory ad hoc query (same filters/types/ordering) was run manually by the project owner and returned 20 real connectivity records, confirming the dataset and query are reachable. That ad hoc run did not go through the checksummed `scripts/retrieve_da1.py` pipeline, so its output is not treated as the authoritative recorded artifact for this entry. |

Exact Cypher query (verbatim, must match `src/flybrain/da1_retrieval.py`'s `CYPHER_QUERY`):

```cypher
MATCH (a:Neuron)-[e:ConnectsTo]->(b:Neuron)
WHERE a.type = 'ORN_DA1'
  AND b.type = 'DA1_lPN'
RETURN
    a.bodyId AS source_body_id,
    a.instance AS source_instance,
    b.bodyId AS target_body_id,
    b.instance AS target_instance,
    e.weight AS synapse_weight
ORDER BY synapse_weight DESC,
         source_body_id ASC,
         target_body_id ASC
LIMIT 20
```

**Update:** the dataset referred to generically as "MaleCNS" elsewhere in
`ROADMAP.md` M1 has now been verified, via a live connection test, as
`male-cns:v1.0` on the Janelia neuPrint instance at
https://neuprint.janelia.org (entry above). Licence and citation
information for this dataset remain PENDING VERIFICATION.
