import requests
import json
import os

from datetime import datetime, UTC


def submit_application():

    run_id = os.environ.get("GITHUB_RUN_ID")

    if run_id is None:
        raise RuntimeError("Could not read action run id")

    body = json.dumps({
        "action_run_link": f"https://github.com/slDias/b12/actions/runs/{run_id}",
        "email": "lucas97dias@outlook.com",
        "name": "Lucas Dias",
        "repository_link": "https://github.com/slDias/b12",
        "resume_link": "https://www.linkedin.com/in/ldias-dev/",
        "timestamp": datetime.now(UTC).isoformat()
    }, separators=(',', ':'))

    return requests.post(
        "https://b12.io/apply/submission",
        data=body.encode("utf-8")
    )
    

if __name__ == "__main__":
    submit_application()
