#!/usr/bin/env python3
"""E001 / M2.1: analyse the selected ORN_DA1 -> DA1_lPN connectivity graph.

Usage:
    python scripts/analyze_da1_graph.py

Reads ONLY the already-retrieved raw artifact named in docs/EXPERIMENT_LOG.md
(E001), verifies its SHA-256 before analysis, builds a directed weighted
graph, runs the E001 validation checks, prints global / per-node /
DA1_lPN-convergence metrics, and saves one static figure under
data/processed/da1/ (git-ignored). Makes no network access and never
modifies the raw CSV.

The graph covers only the selected top-20 strongest edges, not the complete
DA1 circuit. `synapse_weight` is a structural synapse count, not electrical
signal strength.
"""

from __future__ import annotations

import platform
import sys
from importlib.metadata import version
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from flybrain.da1_graph import (  # noqa: E402
    E001_ARTIFACT_PATH,
    E001_SHA256,
    ChecksumMismatchError,
    build_graph,
    convergence_table,
    global_metrics,
    load_edge_table,
    node_metrics,
    validate_graph,
)
from flybrain.da1_graph_plot import plot_selected_graph  # noqa: E402

FIGURE_PATH = REPO_ROOT / "data/processed/da1/m2_1_selected_connectivity.png"


def main() -> int:
    csv_path = REPO_ROOT / E001_ARTIFACT_PATH
    print("E001 / M2.1 - Selected DA1 connectivity graph")
    print(f"Input artifact: {E001_ARTIFACT_PATH}")
    print(
        "Scope: the selected top-20 strongest ORN_DA1 -> DA1_lPN edges only "
        "(not the complete DA1 circuit)."
    )
    print("synapse_weight = structural synapse count, not electrical signal strength.")
    print(
        f"Environment: python {platform.python_version()}, "
        f"networkx {version('networkx')}, pandas {version('pandas')}, "
        f"matplotlib {version('matplotlib')}"
    )

    try:
        table = load_edge_table(csv_path, E001_SHA256)
    except FileNotFoundError:
        print(f"ERROR: input artifact not found: {csv_path}", file=sys.stderr)
        return 1
    except ChecksumMismatchError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"SHA-256 verified before analysis: {E001_SHA256}")

    graph = build_graph(table)

    print("\nVALIDATION")
    checks = validate_graph(graph)
    for check in checks:
        status = "PASS" if check.passed else "FAIL"
        print(f"  [{status}] {check.name}: {check.detail}")
    if not all(check.passed for check in checks):
        print("ERROR: validation failed; no results reported.", file=sys.stderr)
        return 1

    print("\nGLOBAL")
    for name, value in global_metrics(graph).items():
        print(f"  {name}: {value}")

    print("\nPER NODE")
    print(node_metrics(graph).to_string(index=False))

    print("\nDA1_lPN CONVERGENCE (this selected sample only)")
    print(convergence_table(graph).to_string(index=False))

    plot_selected_graph(graph, FIGURE_PATH)
    print(f"\nFigure saved to: {FIGURE_PATH.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
