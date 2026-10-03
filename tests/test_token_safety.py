"""Token safety tests: NEUPRINT_TOKEN must never leak.

These tests use a monkeypatched stand-in for `neuprint.Client`. No real
network request is made and no real neuPrint credentials are used.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone

import pandas as pd
import pytest

from flybrain import neuprint_client
from flybrain.da1_retrieval import build_provenance, fetch_orn_da1_to_da1_lpn, save_raw_csv

FAKE_TOKEN = "super-secret-test-token-should-never-leak"  # nosec: test fixture only


class _RecordingClient:
    """Stand-in for neuprint.Client; records constructor args, no network."""

    def __init__(self, server, dataset=None, token=None):
        self.server = server
        self.dataset = dataset
        self.token = token

    def __repr__(self) -> str:
        return f"_RecordingClient(server={self.server!r}, dataset={self.dataset!r})"

    def fetch_custom(self, cypher):
        # Simulate a "normal" failure unrelated to auth, to check that
        # ordinary error messages never embed the token either.
        raise ValueError("simulated: neuPrint result missing expected columns")


def _sample_table() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "source_body_id": 1,
                "source_instance": "A",
                "target_body_id": 2,
                "target_instance": "B",
                "synapse_weight": 5,
            }
        ]
    )


def test_token_is_read_from_environment_and_passed_to_client(monkeypatch):
    monkeypatch.setenv(neuprint_client.TOKEN_ENV_VAR, FAKE_TOKEN)
    monkeypatch.setattr(neuprint_client, "Client", _RecordingClient)

    client = neuprint_client.get_client()

    assert isinstance(client, _RecordingClient)
    assert client.token == FAKE_TOKEN


def test_token_is_never_printed_or_logged(monkeypatch, capsys):
    monkeypatch.setenv(neuprint_client.TOKEN_ENV_VAR, FAKE_TOKEN)
    monkeypatch.setattr(neuprint_client, "Client", _RecordingClient)

    client = neuprint_client.get_client()
    print(client)  # exercise __repr__, in case logging code ever does this

    captured = capsys.readouterr()
    assert FAKE_TOKEN not in captured.out
    assert FAKE_TOKEN not in captured.err


def test_token_is_not_included_in_provenance(monkeypatch, tmp_path):
    monkeypatch.setenv(neuprint_client.TOKEN_ENV_VAR, FAKE_TOKEN)

    table = _sample_table()
    ts = datetime(2026, 1, 2, 3, 4, 5, tzinfo=timezone.utc)
    csv_path = save_raw_csv(table, tmp_path, timestamp=ts)

    provenance = build_provenance(table=table, csv_path=csv_path, retrieval_timestamp=ts)

    assert FAKE_TOKEN not in json.dumps(provenance)


def test_token_is_not_included_in_normal_error_messages(monkeypatch):
    monkeypatch.setenv(neuprint_client.TOKEN_ENV_VAR, FAKE_TOKEN)
    monkeypatch.setattr(neuprint_client, "Client", _RecordingClient)

    client = neuprint_client.get_client()

    with pytest.raises(ValueError) as exc_info:
        fetch_orn_da1_to_da1_lpn(client)

    assert FAKE_TOKEN not in str(exc_info.value)


def test_missing_token_error_message_contains_no_leftover_secret(monkeypatch):
    # Even an unrelated secret sitting in the environment must not leak
    # into the "token missing" error path.
    monkeypatch.delenv(neuprint_client.TOKEN_ENV_VAR, raising=False)
    monkeypatch.setenv("SOME_OTHER_SECRET", FAKE_TOKEN)

    with pytest.raises(neuprint_client.MissingNeuprintTokenError) as exc_info:
        neuprint_client.get_client()

    assert FAKE_TOKEN not in str(exc_info.value)
