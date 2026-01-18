import requests
import json
import os

from datetime import datetime, UTC
import hmac
import hashlib


def submit_application():

    run_id = os.environ.get("GITHUB_RUN_ID")
    secret = os.environ.get("SECRET")

    if run_id is None:
        raise RuntimeError("Could not read action run id")

    if secret is None:
        raise RuntimeError("Could not read secret")

    body = json.dumps({
        "action_run_link": f"https://github.com/slDias/b12/actions/runs/{run_id}",
        "email": "lucas97dias@outlook.com",
        "name": "Lucas Dias",
        "repository_link": "https://github.com/slDias/b12",
        "resume_link": "https://www.linkedin.com/in/ldias-dev/",
        "timestamp": datetime.now(UTC).isoformat()
    }, separators=(',', ':')).encode("utf-8")

    body_hmac = hmac.new(
        secret.encode(), 
        body, 
        hashlib.sha256
    )

    return requests.post(
        "https://b12.io/apply/submission",
        data=body,
        headers={'sha256': body_hmac.hexdigest()}
    )
    

if __name__ == "__main__":
    response = submit_application()
    print(response.text)
