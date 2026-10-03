"""neuPrint connection and authentication.

This module is responsible ONLY for constructing an authenticated
neuprint-python `Client`. It intentionally contains no connectome
retrieval/query logic (see `da1_retrieval.py` for that).

The auth token is read exclusively from the `NEUPRINT_TOKEN` environment
variable. It is never hard-coded, returned to a caller, printed, logged,
or written to disk by this module.
"""

from __future__ import annotations

import os

from neuprint import Client

DEFAULT_SERVER = "https://neuprint.janelia.org"
DEFAULT_DATASET = "male-cns:v1.0"
TOKEN_ENV_VAR = "NEUPRINT_TOKEN"


class MissingNeuprintTokenError(RuntimeError):
    """Raised when NEUPRINT_TOKEN is not set in the environment."""


def get_client(
    server: str = DEFAULT_SERVER,
    dataset: str = DEFAULT_DATASET,
) -> Client:
    """Build an authenticated neuprint-python Client.

    Reads the auth token only from the `NEUPRINT_TOKEN` environment
    variable. Raises `MissingNeuprintTokenError` (without attempting any
    network connection) if it is not set.
    """
    token = os.environ.get(TOKEN_ENV_VAR)
    if not token:
        raise MissingNeuprintTokenError(
            f"{TOKEN_ENV_VAR} is not set. Export a valid neuPrint auth "
            f"token as the {TOKEN_ENV_VAR} environment variable before "
            f"connecting."
        )
    return Client(server, dataset=dataset, token=token)
