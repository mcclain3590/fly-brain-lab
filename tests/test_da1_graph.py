"""Tests for flybrain.da1_graph.

Synthetic fixtures only (see conftest.py); no network access, credentials, or
real connectome data.
"""

from __future__ import annotations

import networkx as nx
import pandas as pd
import pytest

from flybrain.da1_graph import (
    ChecksumMismatchError,
    build_graph,
    convergence_table,
    global_metrics,
    load_edge_table,
    node_metrics,
    validate_graph,
)
from flybrain.da1_retrieval import EXPECTED_COLUMNS, SOURCE_TYPE, TARGET_TYPE, sha256_of_file

def _write_csv(table: pd.DataFrame, tmp_path):
    path = tmp_path / "edges.csv"
    table.to_csv(path, index=False)
    return path, sha256_of_file(path)


def _failed(checks) -> set[str]:
    return {c.name for c in checks if not c.passed}


# --- loading and checksum -------------------------------------------------


def test_load_returns_table_when_checksum_matches(small_table, tmp_path):
    path, sha = _write_csv(small_table, tmp_path)
    loaded = load_edge_table(path, sha)
    assert len(loaded) == 5
    assert list(loaded.columns) == EXPECTED_COLUMNS


def test_load_rejects_modified_file(small_table, tmp_path):
    path, sha = _write_csv(small_table, tmp_path)
    path.write_text(path.read_text().replace(",5\n", ",6\n", 1))
    with pytest.raises(ChecksumMismatchError):
        load_edge_table(path, sha)


def test_checksum_is_verified_before_the_file_is_parsed(tmp_path):
    path = tmp_path / "garbage.csv"
    path.write_bytes(b"\xff\xfe not,a,valid\x00csv")
    with pytest.raises(ChecksumMismatchError):
        load_edge_table(path, "0" * 64)


def test_load_raises_for_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_edge_table(tmp_path / "absent.csv", "0" * 64)


# --- graph construction ---------------------------------------------------


def test_build_graph_one_node_per_body_id_and_one_edge_per_row(small_table):
    graph = build_graph(small_table)
    assert isinstance(graph, nx.DiGraph)
    assert graph.number_of_nodes() == 6
    assert graph.number_of_edges() == 5


def test_edges_are_directed_source_to_target(small_table):
    graph = build_graph(small_table)
    assert graph.has_edge(1, 20)
    assert not graph.has_edge(20, 1)


def test_edge_carries_synapse_weight(small_table):
    graph = build_graph(small_table)
    assert graph[2][11]["synapse_weight"] == 4
    assert graph[1][20]["synapse_weight"] == 5


def test_node_attributes_identify_body_id_type_and_instance(small_table):
    graph = build_graph(small_table)
    assert graph.nodes[3] == {
        "body_id": 3,
        "neuron_type": SOURCE_TYPE,
        "instance": "ORN_DA1_L",
    }
    assert graph.nodes[20] == {
        "body_id": 20,
        "neuron_type": TARGET_TYPE,
        "instance": "DA1_lPN_R",
    }


def test_missing_instance_becomes_none_after_csv_round_trip(small_table, tmp_path):
    path, sha = _write_csv(small_table, tmp_path)
    graph = build_graph(load_edge_table(path, sha))
    assert graph.nodes[4]["instance"] is None


def test_build_rejects_duplicate_edge(small_table):
    duplicated = pd.concat([small_table, small_table.iloc[[0]]], ignore_index=True)
    with pytest.raises(ValueError, match="duplicate edge"):
        build_graph(duplicated)


# --- metrics --------------------------------------------------------------


def test_global_metrics(small_table):
    assert global_metrics(build_graph(small_table)) == {
        "node_count": 6,
        "edge_count": 5,
        "total_synapse_weight": 15,
    }


def test_node_metrics_values_and_order(small_table):
    metrics = node_metrics(build_graph(small_table))
    assert metrics["body_id"].tolist() == [1, 2, 3, 4, 11, 20]
    assert metrics["neuron_type"].tolist() == [SOURCE_TYPE] * 4 + [TARGET_TYPE] * 2
    numeric = metrics[
        ["in_degree", "out_degree", "total_incoming_weight", "total_outgoing_weight"]
    ]
    assert numeric.values.tolist() == [
        [0, 1, 0, 5],
        [0, 2, 0, 7],
        [0, 1, 0, 2],
        [0, 1, 0, 1],
        [2, 0, 6, 0],
        [3, 0, 9, 0],
    ]


def test_node_metrics_order_does_not_depend_on_row_order(small_table):
    shuffled = small_table.sample(frac=1, random_state=0)
    pd.testing.assert_frame_equal(
        node_metrics(build_graph(shuffled)), node_metrics(build_graph(small_table))
    )


def test_convergence_counts_distinct_orn_sources_and_weight(small_table):
    table = convergence_table(build_graph(small_table))
    assert table["body_id"].tolist() == [20, 11]
    assert table["distinct_orn_da1_sources"].tolist() == [3, 2]
    assert table["total_incoming_weight"].tolist() == [9, 6]


def test_convergence_has_one_row_per_da1_lpn_only(full_shape_table):
    table = convergence_table(build_graph(full_shape_table))
    assert len(table) == 5
    assert set(table["body_id"]) == {2001, 2002, 2003, 2004, 2005}


# --- validation -----------------------------------------------------------


def test_full_shape_graph_passes_every_default_check(full_shape_table):
    checks = validate_graph(build_graph(full_shape_table))
    assert _failed(checks) == set()
    assert {c.name for c in checks} >= {
        "node_count",
        "edge_count",
        "ORN_DA1_node_count",
        "DA1_lPN_node_count",
        "source_target_disjoint",
        "sum_in_degree",
        "sum_out_degree",
        "positive_synapse_weights",
        "weight_conservation",
    }


def test_small_graph_fails_default_e001_counts(small_table):
    assert {"node_count", "edge_count"} <= _failed(validate_graph(build_graph(small_table)))


def test_missing_edge_fails_edge_count_and_degree_sums(full_shape_table):
    graph = build_graph(full_shape_table)
    graph.remove_edge(1001, 2002)
    assert _failed(validate_graph(graph)) == {"edge_count", "sum_in_degree", "sum_out_degree"}


@pytest.mark.parametrize("bad_weight", [0, -3])
def test_non_positive_weight_fails(full_shape_table, bad_weight):
    graph = build_graph(full_shape_table)
    graph[1001][2002]["synapse_weight"] = bad_weight
    assert "positive_synapse_weights" in _failed(validate_graph(graph))


def test_missing_weight_attribute_fails(full_shape_table):
    graph = build_graph(full_shape_table)
    del graph[1001][2002]["synapse_weight"]
    assert "positive_synapse_weights" in _failed(validate_graph(graph))


def test_extra_node_fails_only_node_count(full_shape_table):
    graph = build_graph(full_shape_table)
    graph.add_node(9999, neuron_type="other")
    assert _failed(validate_graph(graph)) == {"node_count"}


def test_wrong_type_counts_fail(full_shape_table):
    graph = build_graph(full_shape_table)
    graph.nodes[1001]["neuron_type"] = TARGET_TYPE
    assert _failed(validate_graph(graph)) == {"ORN_DA1_node_count", "DA1_lPN_node_count"}


def test_body_id_used_as_both_source_and_target_is_reported_by_validation(full_shape_table):
    overlapping = pd.concat(
        [
            full_shape_table,
            pd.DataFrame([(2001, "DA1_lPN_R", 2002, "DA1_lPN_R", 3)], columns=EXPECTED_COLUMNS),
        ],
        ignore_index=True,
    )
    assert "source_target_disjoint" in _failed(validate_graph(build_graph(overlapping)))
