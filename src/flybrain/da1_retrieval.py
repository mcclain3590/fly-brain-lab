"""Deterministic retrieval of ORN_DA1 -> DA1_lPN connectivity.

This module contains ONLY the connectome retrieval logic for the first
selected M1 circuit (ORN_DA1 -> DA1_lPN). It does not handle neuPrint
connection/authentication (see `neuprint_client.py`).

The table returned here is measured/reconstructed biological connectome
data; it is not a computational model. See docs/PROJECT_CHARTER.md Sec 5-6
and docs/ARCHITECTURE.md Sec 2 for why that distinction must be preserved.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _pkg_version
from pathlib import Path
from typing import Any, Protocol

import pandas as pd

from .neuprint_client import DEFAULT_DATASET, DEFAULT_SERVER

SOURCE_TYPE = "ORN_DA1"
TARGET_TYPE = "DA1_lPN"
RESULT_LIMIT = 20

SELECTION_RULE = (
    f"Top {RESULT_LIMIT} ConnectsTo edges from {SOURCE_TYPE} to "
    f"{TARGET_TYPE}, ordered by synapse_weight DESC, then source_body_id "
    f"ASC, then target_body_id ASC."
)

# Exact Cypher query, verbatim as approved by the project owner. Do not
# alter without updating docs/DATA_SOURCES.md and docs/DECISION_LOG.md.
CYPHER_QUERY = f"""\
MATCH (a:Neuron)-[e:ConnectsTo]->(b:Neuron)
WHERE a.type = '{SOURCE_TYPE}'
  AND b.type = '{TARGET_TYPE}'
RETURN
    a.bodyId AS source_body_id,
    a.instance AS source_instance,
    b.bodyId AS target_body_id,
    b.instance AS target_instance,
    e.weight AS synapse_weight
ORDER BY synapse_weight DESC,
         source_body_id ASC,
         target_body_id ASC
LIMIT {RESULT_LIMIT}
"""

EXPECTED_COLUMNS = [
    "source_body_id",
    "source_instance",
    "target_body_id",
    "target_instance",
    "synapse_weight",
]


class FetchCustomClient(Protocol):
    """Structural type for anything exposing neuprint.Client's fetch_custom."""

    def fetch_custom(self, cypher: str) -> pd.DataFrame: ...


def fetch_orn_da1_to_da1_lpn(client: FetchCustomClient) -> pd.DataFrame:
    """Run the exact approved Cypher query and return the raw result.

    The returned DataFrame is untouched beyond what the query itself
    produces: no renaming, re-sorting, filtering, or other transformation
    is applied here. `client` only needs to implement `fetch_custom`, so
    this function can be exercised in tests with a stand-in that performs
    no network access.
    """
    result = client.fetch_custom(CYPHER_QUERY)
    missing = [c for c in EXPECTED_COLUMNS if c not in result.columns]
    if missing:
        raise ValueError(f"neuPrint result is missing expected column(s): {missing}")
    return result


def save_raw_csv(
    table: pd.DataFrame,
    output_dir: Path,
    *,
    timestamp: datetime | None = None,
) -> Path:
    """Save the untouched table as CSV under output_dir, deterministically.

    The filename encodes the UTC retrieval timestamp so repeated runs
    never silently overwrite a prior retrieval's artifact.
    """
    ts = timestamp or datetime.now(timezone.utc)
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = f"orn_da1_to_da1_lpn_{ts.strftime('%Y%m%dT%H%M%SZ')}.csv"
    csv_path = output_dir / filename
    table.to_csv(csv_path, index=False, columns=EXPECTED_COLUMNS)
    return csv_path


def sha256_of_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _neuprint_python_version() -> str:
    try:
        return _pkg_version("neuprint-python")
    except PackageNotFoundError:
        return "UNKNOWN"


def build_provenance(
    *,
    table: pd.DataFrame,
    csv_path: Path,
    row_count: int,
    retrieval_timestamp: datetime,
    server: str = DEFAULT_SERVER,
    dataset: str = DEFAULT_DATASET,
) -> dict[str, Any]:
    """Build the provenance record for one retrieval run.

    Contains no secrets: the auth token is never read or included here.
    """
    unique_source_neurons = int(table["source_body_id"].nunique())
    unique_target_neurons = int(table["target_body_id"].nunique())
    unique_total_neurons = len(
        set(table["source_body_id"]) | set(table["target_body_id"])
    )

    return {
        "source_system": "Janelia neuPrint",
        "endpoint": server,
        "dataset": dataset,
        "source_neuron_type": SOURCE_TYPE,
        "target_neuron_type": TARGET_TYPE,
        "cypher_query": CYPHER_QUERY,
        "selection_rule": SELECTION_RULE,
        "retrieval_timestamp_utc": retrieval_timestamp.isoformat(),
        "neuprint_python_version": _neuprint_python_version(),
        "row_count": row_count,
        "unique_source_neurons": unique_source_neurons,
        "unique_target_neurons": unique_target_neurons,
        "unique_total_neurons": unique_total_neurons,
        "output_filename": csv_path.name,
        "sha256_checksum": sha256_of_file(csv_path),
    }


def save_provenance(provenance: dict[str, Any], csv_path: Path) -> Path:
    provenance_path = csv_path.with_suffix(csv_path.suffix + ".provenance.json")
    provenance_path.write_text(json.dumps(provenance, indent=2, sort_keys=True) + "\n")
    return provenance_path
