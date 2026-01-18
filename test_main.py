import pytest
import responses
import uuid
import os
import json
from responses import matchers
from unittest.mock import patch
from datetime import UTC

from main import submit_application

import hmac
import hashlib


@patch("main.datetime")
@patch.dict(os.environ, {"GITHUB_RUN_ID": uuid.uuid4().hex, "SECRET": uuid.uuid4().hex}, clear=True)
@responses.activate
def test_makes_request(dt_mock):
    expected_time = "2026-01-06T16:59:37.571Z"
    dt_mock.now.return_value.isoformat.return_value = expected_time
    expected_request = {
        "action_run_link": f"https://github.com/slDias/b12/actions/runs/{os.environ.get("GITHUB_RUN_ID")}",
        "email": "lucas97dias@outlook.com",
        "name": "Lucas Dias",
        "repository_link": "https://github.com/slDias/b12",
        "resume_link": "https://www.linkedin.com/in/ldias-dev/",
        "timestamp": expected_time
    }
    expected_request_text = json.dumps(expected_request, separators=(',', ':'))
    expected_response = {"success": True, "receipt": uuid.uuid4().hex}
    body_hmac = hmac.new(os.environ.get("SECRET").encode(), expected_request_text.encode("utf-8"), hashlib.sha256)

    expected_headers = {"X-Signature-256": f"sha256={body_hmac.hexdigest()}"}
    responses.add(
        responses.Response(
            method="POST",
            url="https://b12.io/apply/submission",
            json=expected_response,
            match=[
                matchers.body_matcher(expected_request_text),
                matchers.header_matcher(expected_headers)
            ]
        )
    )

    response = submit_application()

    assert response.json() == expected_response
    dt_mock.now.assert_called_once_with(UTC)
    dt_mock.now.return_value.isoformat.assert_called_once_with()


@patch.dict(os.environ, {"SECRET": uuid.uuid4().hex}, clear=True)
@responses.activate
def test_raises_if_no_id():

    with pytest.raises(RuntimeError, match="Could not read action run id"):
        submit_application()

@patch.dict(os.environ, {"GITHUB_RUN_ID": uuid.uuid4().hex}, clear=True)
@responses.activate
def test_raises_if_no_secret():

    with pytest.raises(RuntimeError, match="Could not read secret"):
        submit_application()

