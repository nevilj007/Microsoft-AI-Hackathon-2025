import os
import requests
from dotenv import load_dotenv
load_dotenv(dotenv_path='config/secrets.env')

GITHUB_API = "https://api.github.com"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")

def check_status(run_id: str) -> dict:
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    url = f"{GITHUB_API}/repos/{GITHUB_REPO}/actions/runs/{run_id}"
    res = requests.get(url, headers=headers)

    if not res.ok:
        raise Exception(f" Failed to check status: {res.status_code} {res.text}")

    data = res.json()

    status = data["status"]
    conclusion = data.get("conclusion")

    return {
        "status": status,
        "conclusion": conclusion,
        "workflow": data["name"],
        "branch": data["head_branch"],
        "url": data["html_url"]
    }
