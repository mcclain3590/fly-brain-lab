# Fly Brain Lab — Data Sources

Status: **PARTIALLY VERIFIED.** M1 — Connectome Access is now IN PROGRESS
(see `ROADMAP.md`). Dataset/endpoint access has been verified live by the
project owner, and the first checksummed retrieval artifact has now been
produced via `scripts/retrieve_da1.py` on the project owner's machine. No
field below may be filled with a guessed, assumed, or remembered value —
fields not yet independently verified are marked PENDING VERIFICATION.

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
| Retrieval date | 2026-10-03T06:24:31.765554+00:00 (UTC) |
| Retrieved by | Sagar (project owner), via `scripts/retrieve_da1.py` |
| Subset retrieved (e.g. neuron count/IDs) | `ORN_DA1 -> DA1_lPN` `ConnectsTo` edges, top 20 by synapse weight. row_count=20, unique_source_neurons=18, unique_target_neurons=5, unique_total_neurons=23 (see retrieved IDs below) |
| Exact query / request or retrieval parameters | See Cypher query below |
| Retrieval script / command or code entry point | `scripts/retrieve_da1.py` (`src/flybrain/neuprint_client.py`, `src/flybrain/da1_retrieval.py`) |
| Filtering criteria applied | `a.type = 'ORN_DA1' AND b.type = 'DA1_lPN'`, ordered by `synapse_weight DESC, source_body_id ASC, target_body_id ASC`, `LIMIT 20` |
| Retrieved neuron/record IDs (exact list, where practical) | See table below. Sourced from an exploratory run of the identical query/filters shown earlier in the AI engineering session that produced this code — its summary statistics (20 rows, 18 unique source IDs, 5 unique target IDs, 23 unique total, no source/target overlap) match the authoritative run's reported statistics exactly, which is why it is recorded here. This listing has **not** been independently byte-verified against the checksummed CSV itself (that file was intentionally never transferred off the project owner's machine — see Notes). |
| Local raw artifact path | `data/raw/da1/orn_da1_to_da1_lpn_20261003T062431Z.csv` (git-ignored; see `.gitignore` — the file itself is not committed) |
| Checksum / hash of retrieved artifact | SHA-256: `23354c46fec504b4c338c73d1eb3cd8167b4fdca8cfd7a880fbccd9df98fa2fc` (as reported by the project owner from the live run; not independently recomputed by Claude Code, since the raw CSV was never transferred to this environment) |
| Schema / field snapshot or notes | `source_body_id`, `source_instance`, `target_body_id`, `target_instance`, `synapse_weight` (as returned by the Cypher query) |
| Transformations applied, if any | None — the raw query result is saved untouched |
| Notes / caveats | neuprint-python 0.6.3, pandas 3.0.6, Python 3.12.8 were the validated versions on the retrieval machine (see `README.md`). The raw CSV is intentionally **not** committed to the repository (per project policy); only this provenance record and the matching `.provenance.json` written alongside the CSV on the retrieval machine capture what was retrieved. |

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

Retrieved rows (see provenance note above on how this listing was sourced
and its verification limits):

| source_body_id | source_instance | target_body_id | target_instance | synapse_weight |
|---|---|---|---|---|
| 181663 | ORN_DA1_R | 11780 | DA1_lPN_R | 64 |
| 120209 | ORN_DA1_R | 11780 | DA1_lPN_R | 60 |
| 152946 | ORN_DA1_R | 11780 | DA1_lPN_R | 52 |
| 167423 | ORN_DA1_R | 12122 | DA1_lPN_R | 50 |
| 128233 | ORN_DA1_R | 12122 | DA1_lPN_R | 49 |
| 152946 | ORN_DA1_R | 11996 | DA1_lPN_R | 49 |
| 193957 | ORN_DA1_R | 11816 | DA1_lPN_R | 49 |
| 925289 | ORN_DA1_R | 11996 | DA1_lPN_R | 49 |
| 140055 | ORN_DA1_R | 11780 | DA1_lPN_R | 48 |
| 157253 | ORN_DA1_R | 13064 | DA1_lPN_R | 48 |
| 118367 | ORN_DA1_R | 11780 | DA1_lPN_R | 47 |
| 118367 | ORN_DA1_R | 12122 | DA1_lPN_R | 47 |
| 128088 | ORN_DA1_R | 12122 | DA1_lPN_R | 47 |
| 132713 | ORN_DA1_R | 11780 | DA1_lPN_R | 47 |
| 133686 | ORN_DA1_R | 11780 | DA1_lPN_R | 47 |
| 159263 | ORN_DA1_R | 11816 | DA1_lPN_R | 47 |
| 108716 | ORN_DA1_R | 11996 | DA1_lPN_R | 46 |
| 122707 | ORN_DA1_R | 11816 | DA1_lPN_R | 46 |
| 126030 | ORN_DA1_R | 12122 | DA1_lPN_R | 46 |
| 200896 | ORN_DA1_L | 13064 | DA1_lPN_R | 46 |

Independently recomputed from this listing: 18 unique `source_body_id`
values, 5 unique `target_body_id` values, 23 unique values across both
columns (no overlap between the source and target ID sets) — consistent
with the authoritative run's reported counts.

**Update:** the dataset referred to generically as "MaleCNS" elsewhere in
`ROADMAP.md` M1 has now been verified, via a live connection test and a
completed checksummed retrieval, as `male-cns:v1.0` on the Janelia neuPrint
instance at https://neuprint.janelia.org (entry above). Licence and
citation information for this dataset remain PENDING VERIFICATION.
