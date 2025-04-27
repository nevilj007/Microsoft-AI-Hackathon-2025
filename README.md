#  BuildBot (Zero-Cost CI/CD Assistant)

A lightweight AI-powered assistant to trigger builds, monitor status, and summarize logs — all for **$0**.

##  Requirements

- GitHub repo with Actions
- GitHub personal access token (PAT)
- Python 3.8+
- u need this in ur workflow the permissions for auto dispatch:
for eg:
on:
  workflow_dispatch:
    inputs:
      tag:
        description: "Docker image tag"
        required: false
        default: "latest"

##  Getting Started

```bash
pip install -r requirements.txt
export $(cat config/secrets.env | xargs)
python cli/main.py




