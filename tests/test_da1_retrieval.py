"""Tests for flybrain.da1_retrieval.

These tests must not require network access or neuPrint credentials. They
use an in-memory pandas DataFrame and a fake client instead of a real
neuprint-python Client or real connectome data.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone

import pandas as pd
import pytest

from flybrain.da1_retrieval import (
    CYPHER_QUERY,
    RESULT_LIMIT,
    SOURCE_TYPE,
    TARGET_TYPE,
    build_provenance,
    fetch_orn_da1_to_da1_lpn,
    save_provenance,
    save_raw_csv,
    sha256_of_file,
)


class _FakeClient:
    """Stand-in for neuprint.Client.fetch_custom; no network access."""

    def __init__(self, table: pd.DataFrame):
        self._table = table
        self.last_query = None

    def fetch_custom(self, cypher):
        self.last_query = cypher
        return self._table


def _sample_table() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "source_body_id": 181663,
                "source_instance": "ORN_DA1_R",
                "target_body_id": 11780,
                "target_instance": "DA1_lPN_R",
                "synapse_weight": 64,
            },
            {
                "source_body_id": 120209,
                "source_instance": "ORN_DA1_R",
                "target_body_id": 11780,
                "target_instance": "DA1_lPN_R",
                "synapse_weight": 60,
            },
        ]
    )


def test_query_targets_exact_approved_types_and_limit():
    assert "a.type = 'ORN_DA1'" in CYPHER_QUERY
    assert "b.type = 'DA1_lPN'" in CYPHER_QUERY
    assert f"LIMIT {RESULT_LIMIT}" in CYPHER_QUERY
    assert SOURCE_TYPE == "ORN_DA1"
    assert TARGET_TYPE == "DA1_lPN"
    assert RESULT_LIMIT == 20


def test_fetch_runs_exact_query_and_returns_untouched_table():
    table = _sample_table()
    client = _FakeClient(table)

    result = fetch_orn_da1_to_da1_lpn(client)

    assert client.last_query == CYPHER_QUERY
    pd.testing.assert_frame_equal(result, table)


def test_fetch_rejects_result_missing_expected_columns():
    bad_table = _sample_table().drop(columns=["synapse_weight"])
    client = _FakeClient(bad_table)

    with pytest.raises(ValueError):
        fetch_orn_da1_to_da1_lpn(client)


def test_save_raw_csv_is_deterministic_and_untouched(tmp_path):
    table = _sample_table()
    ts = datetime(2026, 1, 2, 3, 4, 5, tzinfo=timezone.utc)

    csv_path = save_raw_csv(table, tmp_path, timestamp=ts)

    assert csv_path.name == "orn_da1_to_da1_lpn_20260102T030405Z.csv"
    reloaded = pd.read_csv(csv_path)
    pd.testing.assert_frame_equal(reloaded, table)


def test_build_and_save_provenance_contains_no_secret_and_matches_file(tmp_path):
    table = _sample_table()
    ts = datetime(2026, 1, 2, 3, 4, 5, tzinfo=timezone.utc)
    csv_path = save_raw_csv(table, tmp_path, timestamp=ts)

    provenance = build_provenance(
        table=table,
        csv_path=csv_path,
        row_count=len(table),
        retrieval_timestamp=ts,
    )

    assert provenance["source_system"] == "Janelia neuPrint"
    assert provenance["source_neuron_type"] == SOURCE_TYPE
    assert provenance["target_neuron_type"] == TARGET_TYPE
    assert provenance["cypher_query"] == CYPHER_QUERY
    assert provenance["row_count"] == len(table)
    # sample table: source_body_id {181663, 120209}, target_body_id {11780}
    assert provenance["unique_source_neurons"] == 2
    assert provenance["unique_target_neurons"] == 1
    assert provenance["unique_total_neurons"] == 3
    assert provenance["output_filename"] == csv_path.name
    assert provenance["sha256_checksum"] == sha256_of_file(csv_path)

    serialized = json.dumps(provenance)
    assert "token" not in serialized.lower()

    provenance_path = save_provenance(provenance, csv_path)
    assert provenance_path.exists()
    assert json.loads(provenance_path.read_text()) == provenance


def test_unique_neuron_counts_handle_overlap_between_source_and_target(tmp_path):
    # body_id 200 appears as a target in row 1 and as a source in row 2,
    # so it must be counted once (not twice) in unique_total_neurons.
    table = pd.DataFrame(
        [
            {
                "source_body_id": 100,
                "source_instance": "A",
                "target_body_id": 200,
                "target_instance": "B",
                "synapse_weight": 10,
            },
            {
                "source_body_id": 200,
                "source_instance": "B",
                "target_body_id": 300,
                "target_instance": "C",
                "synapse_weight": 5,
            },
        ]
    )
    ts = datetime(2026, 1, 2, 3, 4, 5, tzinfo=timezone.utc)
    csv_path = save_raw_csv(table, tmp_path, timestamp=ts)

    provenance = build_provenance(
        table=table,
        csv_path=csv_path,
        row_count=len(table),
        retrieval_timestamp=ts,
    )

    assert provenance["unique_source_neurons"] == 2  # {100, 200}
    assert provenance["unique_target_neurons"] == 2  # {200, 300}
    assert provenance["unique_total_neurons"] == 3  # {100, 200, 300}
