import os
import requests
from dotenv import load_dotenv
load_dotenv(dotenv_path='config/secrets.env')

GITHUB_API = "https://api.github.com"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")  # username/repo

def list_branches_in_repo():
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    url = f"{GITHUB_API}/repos/{GITHUB_REPO}/branches"
    res = requests.get(url, headers=headers)

    if not res.ok:
        raise Exception(f"❌ Could not list branches: {res.status_code} {res.text}")

    branches = res.json()
    return [b["name"] for b in branches]
