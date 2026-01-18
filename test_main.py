import pytest
import responses
import uuid
import os
import json
from responses import matchers
from unittest.mock import patch
from datetime import UTC

from main import submit_application

@patch("main.datetime")
@patch.dict(os.environ, {"GITHUB_RUN_ID": "id_placeholder"}, clear=True)
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
    responses.add(
        responses.Response(
            method="POST",
            url="https://b12.io/apply/submission",
            json=expected_response,
            match=[
                matchers.body_matcher(expected_request_text)
            ]
        )
    )

    response = submit_application()

    assert response.json() == expected_response
    dt_mock.now.assert_called_once_with(UTC)
    dt_mock.now.return_value.isoformat.assert_called_once_with()


@responses.activate
def test_raises_if_no_id():

    with pytest.raises(RuntimeError):
        submit_application()
