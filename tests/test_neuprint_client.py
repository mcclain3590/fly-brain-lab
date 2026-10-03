"""Tests for flybrain.neuprint_client.

These tests must not require network access or a real NEUPRINT_TOKEN.
"""

import pytest

from flybrain.neuprint_client import (
    DEFAULT_DATASET,
    DEFAULT_SERVER,
    TOKEN_ENV_VAR,
    MissingNeuprintTokenError,
    get_client,
)


def test_missing_token_raises_without_network_access(monkeypatch):
    monkeypatch.delenv(TOKEN_ENV_VAR, raising=False)
    with pytest.raises(MissingNeuprintTokenError):
        get_client()


def test_error_message_names_env_var_not_a_token_value(monkeypatch):
    monkeypatch.delenv(TOKEN_ENV_VAR, raising=False)
    with pytest.raises(MissingNeuprintTokenError) as exc_info:
        get_client()
    assert TOKEN_ENV_VAR in str(exc_info.value)


def test_defaults_match_approved_dataset():
    assert DEFAULT_SERVER == "https://neuprint.janelia.org"
    assert DEFAULT_DATASET == "male-cns:v1.0"
