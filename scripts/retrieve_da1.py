#!/usr/bin/env python3
"""Retrieve the top 20 ORN_DA1 -> DA1_lPN ConnectsTo edges from neuPrint.

Usage:
    NEUPRINT_TOKEN=<token> python scripts/retrieve_da1.py

Requires network access to the neuPrint server and a valid NEUPRINT_TOKEN
environment variable (see src/flybrain/neuprint_client.py). Saves the
untouched result as CSV under data/raw/da1/ (git-ignored), together with a
provenance JSON file recording source, query, timestamp, and checksum (see
docs/DATA_SOURCES.md). Never prints, logs, or saves the auth token.
"""

from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from flybrain.da1_retrieval import (  # noqa: E402
    ARTIFACT_SUBDIR,
    build_provenance,
    fetch_orn_da1_to_da1_lpn,
    save_provenance,
    save_raw_csv,
)
from flybrain.neuprint_client import (  # noqa: E402
    DEFAULT_DATASET,
    DEFAULT_SERVER,
    get_client,
)

OUTPUT_DIR = REPO_ROOT / ARTIFACT_SUBDIR


def main() -> int:
    client = get_client()
    table = fetch_orn_da1_to_da1_lpn(client)

    retrieval_timestamp = datetime.now(timezone.utc)
    csv_path = save_raw_csv(table, OUTPUT_DIR, timestamp=retrieval_timestamp)
    provenance = build_provenance(
        table=table,
        csv_path=csv_path,
        retrieval_timestamp=retrieval_timestamp,
        server=DEFAULT_SERVER,
        dataset=DEFAULT_DATASET,
    )
    provenance_path = save_provenance(provenance, csv_path)

    print(f"Retrieved {len(table)} rows.")
    print(f"Saved raw data to:   {csv_path}")
    print(f"Saved provenance to: {provenance_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
