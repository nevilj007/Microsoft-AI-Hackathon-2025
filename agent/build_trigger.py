import os
import requests
from dotenv import load_dotenv
load_dotenv(dotenv_path='config/secrets.env')





GITHUB_API = "https://api.github.com"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")  # Format: username/repo

def trigger_workflow(workflow_filename: str, ref="main", inputs=None):
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    url = f"{GITHUB_API}/repos/{GITHUB_REPO}/actions/workflows/{workflow_filename}/dispatches"
    data = {"ref": ref}

    if inputs:
        data["inputs"] = inputs  # must match workflow_dispatch.inputs in the YAML

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 204:
        print(f" Successfully triggered workflow: `{workflow_filename}` on `{ref}` branch.")
    else:
        print(f" Failed to trigger workflow: {response.status_code} {response.text}")
