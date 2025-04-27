import os
import requests
from dotenv import load_dotenv
load_dotenv(dotenv_path='config/secrets.env')

GITHUB_API = "https://api.github.com"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")  # Format: username/repo

def list_workflows_in_repo():
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    url = f"{GITHUB_API}/repos/{GITHUB_REPO}/contents/.github/workflows"
    res = requests.get(url, headers=headers)

    if not res.ok:
        raise Exception(f" Could not list workflow files: {res.status_code} {res.text}")

    files = res.json()

    workflow_files = [f["name"] for f in files if f["name"].endswith(".yml") or f["name"].endswith(".yaml")]
    return workflow_files
