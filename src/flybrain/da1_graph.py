"""Directed weighted graph of the selected ORN_DA1 -> DA1_lPN edges (E001 / M2.1).

Loads the checksummed raw CSV written by M1.1 (see `da1_retrieval.py`),
builds a directed weighted NetworkX graph, computes structural connectivity
metrics, and validates the result against the E001 pre-run criteria in
docs/EXPERIMENT_LOG.md.

Scientific boundaries (docs/PROJECT_CHARTER.md Sec 5-6):

- The graph describes ONLY the selected top-20 strongest edges retrieved in
  M1.1. It is not the complete DA1 circuit, and no metric computed here may
  be described as a property of the complete circuit.
- `synapse_weight` is the neuPrint structural synapse count for a
  connection. It is measured/reconstructed biological data, NOT electrical
  signal strength, and no neuron dynamics are assumed here.
- The CSV has no neuron-type column. Each node's `neuron_type` comes from the
  retrieval query's type filters (sources are ORN_DA1, targets are DA1_lPN;
  see `da1_retrieval.CYPHER_QUERY`), not from parsing `instance` strings.

This module does not query neuPrint, modify the CSV, or plot (see
`da1_graph_plot.py`).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import networkx as nx
import pandas as pd

from .da1_retrieval import ARTIFACT_SUBDIR, SOURCE_TYPE, TARGET_TYPE, sha256_of_file

WEIGHT = "synapse_weight"

# The single authoritative input artifact for E001 (docs/EXPERIMENT_LOG.md).
E001_ARTIFACT_PATH = ARTIFACT_SUBDIR / "orn_da1_to_da1_lpn_20261003T062431Z.csv"
E001_SHA256 = "23354c46fec504b4c338c73d1eb3cd8167b4fdca8cfd7a880fbccd9df98fa2fc"

# Known properties of the E001 artifact (docs/DATA_SOURCES.md, E001 Phase A).
E001_NODE_COUNT = 23
E001_EDGE_COUNT = 20
E001_SOURCE_NODE_COUNT = 18
E001_TARGET_NODE_COUNT = 5


class ChecksumMismatchError(RuntimeError):
    """The input file's SHA-256 does not match the authoritative checksum."""


@dataclass(frozen=True)
class ValidationCheck:
    name: str
    passed: bool
    detail: str


def load_edge_table(csv_path: Path, expected_sha256: str) -> pd.DataFrame:
    """Verify the file's SHA-256, and only then parse it.

    Raises `ChecksumMismatchError` before any parsing if the checksum does
    not match, so a wrong or modified file is never analysed. The checksum
    pins the exact file contents, so no further content checks are made.
    """
    actual = sha256_of_file(csv_path)
    if actual != expected_sha256:
        raise ChecksumMismatchError(
            f"SHA-256 mismatch for {csv_path}: expected {expected_sha256}, got {actual}"
        )
    return pd.read_csv(csv_path)


def _instance_name(value: object) -> str | None:
    return None if pd.isna(value) else str(value)


def build_graph(table: pd.DataFrame) -> nx.DiGraph:
    """One node per body ID, one directed edge per table row.

    Raises `ValueError` on a repeated (source, target) pair, which a
    `DiGraph` would silently merge. A body ID used as both source and target
    is not rejected here; `validate_graph` reports it.
    """
    graph = nx.DiGraph()
    for row in table.itertuples(index=False):
        source = int(row.source_body_id)
        target = int(row.target_body_id)
        if graph.has_edge(source, target):
            raise ValueError(f"duplicate edge {source} -> {target}")
        graph.add_node(
            source,
            body_id=source,
            neuron_type=SOURCE_TYPE,
            instance=_instance_name(row.source_instance),
        )
        graph.add_node(
            target,
            body_id=target,
            neuron_type=TARGET_TYPE,
            instance=_instance_name(row.target_instance),
        )
        graph.add_edge(source, target, **{WEIGHT: int(row.synapse_weight)})
    return graph


def global_metrics(graph: nx.DiGraph) -> dict[str, int]:
    return {
        "node_count": graph.number_of_nodes(),
        "edge_count": graph.number_of_edges(),
        "total_synapse_weight": sum(w for _, _, w in graph.edges(data=WEIGHT)),
    }


def node_metrics(graph: nx.DiGraph) -> pd.DataFrame:
    """Per-node degree and total synapse weight, ORN_DA1 first, then by body ID."""
    ordered = sorted(
        graph.nodes(data=True),
        key=lambda item: (item[1]["neuron_type"] != SOURCE_TYPE, item[0]),
    )
    return pd.DataFrame(
        {
            "body_id": body_id,
            "neuron_type": attrs["neuron_type"],
            "instance": attrs["instance"],
            "in_degree": graph.in_degree(body_id),
            "out_degree": graph.out_degree(body_id),
            "total_incoming_weight": graph.in_degree(body_id, weight=WEIGHT),
            "total_outgoing_weight": graph.out_degree(body_id, weight=WEIGHT),
        }
        for body_id, attrs in ordered
    )


def convergence_table(graph: nx.DiGraph) -> pd.DataFrame:
    """For each DA1_lPN: distinct ORN_DA1 sources and their total synapse weight.

    Every predecessor of a DA1_lPN node is an ORN_DA1 node (`build_graph`
    types all edge sources that way), so these are the node's in-degree and
    weighted in-degree. Ordered by total incoming weight (descending), then
    body ID. Counts only this selected sample, not the complete DA1 circuit.
    """
    rows = [
        {
            "body_id": body_id,
            "instance": attrs["instance"],
            "distinct_orn_da1_sources": graph.in_degree(body_id),
            "total_incoming_weight": graph.in_degree(body_id, weight=WEIGHT),
        }
        for body_id, attrs in graph.nodes(data=True)
        if attrs["neuron_type"] == TARGET_TYPE
    ]
    rows.sort(key=lambda r: (-r["total_incoming_weight"], r["body_id"]))
    return pd.DataFrame(rows)


def _check(name: str, actual: object, expected: object) -> ValidationCheck:
    return ValidationCheck(name, actual == expected, f"expected {expected}, got {actual}")


def validate_graph(graph: nx.DiGraph) -> list[ValidationCheck]:
    """Run every E001 pre-run validation check and report each result.

    Compares against the known E001 artifact properties. Never raises on a
    failed check; the caller decides what to do.
    """
    neuron_types = [t for _, t in graph.nodes(data="neuron_type")]
    both_roles = [
        n for n in graph if graph.in_degree(n) > 0 and graph.out_degree(n) > 0
    ]
    non_positive = [
        (u, v, w) for u, v, w in graph.edges(data=WEIGHT, default=0) if not w > 0
    ]
    total_edge_weight = sum(w for _, _, w in graph.edges(data=WEIGHT, default=0))
    total_in_weight = sum(w for _, w in graph.in_degree(weight=WEIGHT))
    total_out_weight = sum(w for _, w in graph.out_degree(weight=WEIGHT))

    return [
        _check("node_count", graph.number_of_nodes(), E001_NODE_COUNT),
        _check("edge_count", graph.number_of_edges(), E001_EDGE_COUNT),
        _check(f"{SOURCE_TYPE}_node_count", neuron_types.count(SOURCE_TYPE), E001_SOURCE_NODE_COUNT),
        _check(f"{TARGET_TYPE}_node_count", neuron_types.count(TARGET_TYPE), E001_TARGET_NODE_COUNT),
        ValidationCheck(
            "source_target_disjoint",
            not both_roles,
            f"{len(both_roles)} node(s) have both incoming and outgoing edges",
        ),
        _check("sum_in_degree", sum(d for _, d in graph.in_degree()), E001_EDGE_COUNT),
        _check("sum_out_degree", sum(d for _, d in graph.out_degree()), E001_EDGE_COUNT),
        ValidationCheck(
            "positive_synapse_weights",
            not non_positive,
            f"{len(non_positive)} edge(s) with a missing or non-positive weight",
        ),
        ValidationCheck(
            "weight_conservation",
            total_in_weight == total_out_weight == total_edge_weight,
            f"incoming {total_in_weight}, outgoing {total_out_weight}, "
            f"edge total {total_edge_weight}",
        ),
    ]
