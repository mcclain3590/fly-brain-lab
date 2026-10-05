"""Tests for flybrain.da1_graph_plot.

Synthetic fixtures only (see conftest.py). These check layout logic and that
a valid PNG is produced; they do not judge visual quality.
"""

from __future__ import annotations

from flybrain.da1_graph import build_graph
from flybrain.da1_graph_plot import bipartite_positions, plot_selected_graph
from flybrain.da1_retrieval import SOURCE_TYPE

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def test_sources_are_on_the_left_and_targets_on_the_right(full_shape_table):
    graph = build_graph(full_shape_table)
    positions = bipartite_positions(graph)
    assert set(positions) == set(graph.nodes)
    for node, neuron_type in graph.nodes(data="neuron_type"):
        assert positions[node][0] == (0.0 if neuron_type == SOURCE_TYPE else 1.0)


def test_no_two_nodes_share_a_position(full_shape_table):
    positions = bipartite_positions(build_graph(full_shape_table))
    assert len(set(positions.values())) == len(positions)


def test_layout_does_not_depend_on_row_order(full_shape_table):
    shuffled = full_shape_table.sample(frac=1, random_state=1)
    assert bipartite_positions(build_graph(shuffled)) == bipartite_positions(
        build_graph(full_shape_table)
    )


def test_heaviest_target_is_on_top_and_sources_sit_beside_their_heaviest_target(small_table):
    positions = bipartite_positions(build_graph(small_table))
    assert positions[20][1] > positions[11][1]
    sources_top_to_bottom = sorted((1, 2, 3, 4), key=lambda n: -positions[n][1])
    assert sources_top_to_bottom == [1, 4, 2, 3]


def test_plot_writes_a_png_and_creates_parent_directories(full_shape_table, tmp_path):
    output = tmp_path / "nested" / "figure.png"
    returned = plot_selected_graph(build_graph(full_shape_table), output)
    assert returned == output
    assert output.read_bytes().startswith(PNG_MAGIC)
    assert output.stat().st_size > 10_000
