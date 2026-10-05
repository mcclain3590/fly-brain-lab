"""Shared fixtures for the M2.1 graph tests.

All data here is SYNTHETIC. None of these body IDs, instances, or weights are
real connectome values, and no test asserts anything about the real E001
artifact (which is git-ignored and absent from CI/Claude environments).
"""

from __future__ import annotations

import pandas as pd
import pytest

from flybrain.da1_retrieval import EXPECTED_COLUMNS


@pytest.fixture
def small_table() -> pd.DataFrame:
    """Hand-computable: 4 ORN_DA1 sources, 2 DA1_lPN targets, 5 edges.

    Expected: 6 nodes, 5 edges, total weight 15. Target 20 receives
    5 + 3 + 1 = 9 from 3 sources; target 11 receives 4 + 2 = 6 from 2
    sources. Source 4 has no instance (missing value).
    """
    rows = [
        (1, "ORN_DA1_R", 20, "DA1_lPN_R", 5),
        (2, "ORN_DA1_R", 20, "DA1_lPN_R", 3),
        (2, "ORN_DA1_R", 11, "DA1_lPN_R", 4),
        (3, "ORN_DA1_L", 11, "DA1_lPN_R", 2),
        (4, None, 20, "DA1_lPN_R", 1),
    ]
    return pd.DataFrame(rows, columns=EXPECTED_COLUMNS)


@pytest.fixture
def full_shape_table() -> pd.DataFrame:
    """Synthetic table with the same SHAPE as the E001 artifact.

    18 sources, 5 targets, 23 nodes, 20 edges, disjoint roles, positive
    weights -- so the default E001 validation counts can be exercised.
    """
    rows = [
        (1001 + i, "ORN_DA1_R", 2001 + i % 5, "DA1_lPN_R", 10 + i) for i in range(18)
    ]
    rows += [
        (1001, "ORN_DA1_R", 2002, "DA1_lPN_R", 7),
        (1002, "ORN_DA1_R", 2003, "DA1_lPN_R", 8),
    ]
    return pd.DataFrame(rows, columns=EXPECTED_COLUMNS)
