"""Static bipartite figure of the selected ORN_DA1 -> DA1_lPN graph (E001 / M2.1).

ORN_DA1 neurons are drawn in a left column, DA1_lPN neurons in a right
column, and every directed edge runs left -> right. Clarity is prioritised
over aesthetics.

Edge width and the number printed on each edge are the neuPrint structural
synapse count (`synapse_weight`) -- measured connectivity, not simulated or
electrical signal strength. The figure shows only the selected top-20
subset, not the complete DA1 circuit, and says so on the figure.
"""

from __future__ import annotations

from pathlib import Path

import networkx as nx
from matplotlib.figure import Figure

from .da1_graph import WEIGHT
from .da1_retrieval import RESULT_LIMIT, SOURCE_TYPE, TARGET_TYPE
from .neuprint_client import DEFAULT_DATASET

NODE_SIZE = 260
_LABEL_OFFSET = 0.04
_MIN_EDGE_WIDTH = 0.6
_MAX_EDGE_WIDTH = 4.0
# Edge-label positions along an edge. Verified by rendering: a small value puts
# the label near the source (left) end, where edges are well separated; near
# the target they pile up. A source's heaviest edge is labelled near the source;
# its other (cross-column) edges are labelled mid-edge so they cannot land on a
# neighbouring source's label.
_PRIMARY_LABEL_POS = 0.2
_SECONDARY_LABEL_POS = 0.5


def _column_y(count: int) -> list[float]:
    return [1 - i / (count - 1) for i in range(count)]


def _ordered_targets(graph: nx.DiGraph) -> list[int]:
    return sorted(
        (n for n, t in graph.nodes(data="neuron_type") if t == TARGET_TYPE),
        key=lambda n: (-graph.in_degree(n, weight=WEIGHT), n),
    )


def _heaviest_target(graph: nx.DiGraph, source: int, target_rank: dict[int, int]) -> int:
    return max(
        graph.successors(source),
        key=lambda t: (graph[source][t][WEIGHT], -target_rank[t]),
    )


def bipartite_positions(graph: nx.DiGraph) -> dict[int, tuple[float, float]]:
    """Deterministic layout: ORN_DA1 at x=0, DA1_lPN at x=1.

    Targets are ordered top to bottom by total incoming weight. Each source
    is placed beside its heaviest target to reduce edge crossings; remaining
    ties break on body ID, so the layout never depends on iteration order.
    """
    targets = _ordered_targets(graph)
    target_rank = {n: i for i, n in enumerate(targets)}

    def source_key(node: int) -> tuple[int, int, int]:
        heaviest = _heaviest_target(graph, node, target_rank)
        return (target_rank[heaviest], -graph[node][heaviest][WEIGHT], node)

    sources = sorted(
        (n for n, t in graph.nodes(data="neuron_type") if t == SOURCE_TYPE),
        key=source_key,
    )

    positions = {n: (0.0, y) for n, y in zip(sources, _column_y(len(sources)))}
    positions.update({n: (1.0, y) for n, y in zip(targets, _column_y(len(targets)))})
    return positions


def _label(graph: nx.DiGraph, node: int) -> str:
    instance = graph.nodes[node]["instance"]
    return f"{node}  ({instance})" if instance else str(node)


def plot_selected_graph(graph: nx.DiGraph, output_path: Path) -> Path:
    """Draw the graph to `output_path` (PNG) and return the path."""
    positions = bipartite_positions(graph)
    sources = [n for n, t in graph.nodes(data="neuron_type") if t == SOURCE_TYPE]
    targets = [n for n, t in graph.nodes(data="neuron_type") if t == TARGET_TYPE]
    weights = {(u, v): w for u, v, w in graph.edges(data=WEIGHT)}
    max_weight = max(weights.values())
    edge_widths = [
        _MIN_EDGE_WIDTH + (_MAX_EDGE_WIDTH - _MIN_EDGE_WIDTH) * weights[e] / max_weight
        for e in graph.edges
    ]

    figure = Figure(figsize=(12, 9))
    ax = figure.subplots()
    figure.subplots_adjust(left=0.01, right=0.99, top=0.92, bottom=0.10)
    nx.draw_networkx_edges(
        graph,
        positions,
        ax=ax,
        width=edge_widths,
        edge_color="0.45",
        arrows=True,
        arrowstyle="-|>",
        arrowsize=12,
        node_size=NODE_SIZE,
    )
    nx.draw_networkx_nodes(
        graph, positions, nodelist=sources, node_color="#4c78a8", node_size=NODE_SIZE, ax=ax
    )
    nx.draw_networkx_nodes(
        graph, positions, nodelist=targets, node_color="#e45756", node_size=NODE_SIZE, ax=ax
    )
    target_rank = {n: i for i, n in enumerate(_ordered_targets(graph))}
    primary_edges = {(s, _heaviest_target(graph, s, target_rank)) for s in sources}
    for edge_labels, label_pos in (
        ({e: w for e, w in weights.items() if e in primary_edges}, _PRIMARY_LABEL_POS),
        ({e: w for e, w in weights.items() if e not in primary_edges}, _SECONDARY_LABEL_POS),
    ):
        if edge_labels:
            nx.draw_networkx_edge_labels(
                graph,
                positions,
                edge_labels=edge_labels,
                label_pos=label_pos,
                font_size=7,
                rotate=False,
                bbox={"boxstyle": "round,pad=0.12", "fc": "white", "ec": "none", "alpha": 0.85},
                node_size=NODE_SIZE,
                ax=ax,
            )
    for node in sources:
        x, y = positions[node]
        ax.text(x - _LABEL_OFFSET, y, _label(graph, node), ha="right", va="center", fontsize=8)
    for node in targets:
        x, y = positions[node]
        ax.text(x + _LABEL_OFFSET, y, _label(graph, node), ha="left", va="center", fontsize=8)

    ax.text(0.0, 1.07, f"{SOURCE_TYPE} (n={len(sources)})", ha="center", fontsize=11, weight="bold")
    ax.text(1.0, 1.07, f"{TARGET_TYPE} (n={len(targets)})", ha="center", fontsize=11, weight="bold")
    ax.set_xlim(-0.4, 1.4)
    ax.set_ylim(-0.12, 1.14)
    ax.set_axis_off()

    figure.suptitle(
        f"Selected DA1 connectivity: top {RESULT_LIMIT} strongest "
        f"{SOURCE_TYPE} → {TARGET_TYPE} edges",
        fontsize=13,
        weight="bold",
    )
    figure.text(
        0.5,
        0.02,
        f"Dataset: {DEFAULT_DATASET} (Janelia neuPrint). Selected subset only — "
        "not the complete DA1 circuit.\n"
        "Edge width and edge number = structural synapse count (neuPrint "
        "connection weight), not electrical signal strength.",
        ha="center",
        fontsize=9,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_path, dpi=150)
    return output_path
