import os
import argparse
import requests
from agent.log_summarizer import summarize_logs
from dotenv import load_dotenv

# Load secrets
load_dotenv(dotenv_path='config/secrets.env')

GITHUB_API = "https://api.github.com"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")  # Format: username/repo


def get_latest_run_id():
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    url = f"{GITHUB_API}/repos/{GITHUB_REPO}/actions/runs"
    res = requests.get(url, headers=headers)

    if not res.ok:
        raise Exception(f" Failed to get latest run: {res.status_code} {res.text}")

    runs = res.json().get("workflow_runs", [])
    if not runs:
        raise Exception("No workflow runs found.")

    latest_run_id = runs[0]["id"]
    print(f" Latest run ID: {latest_run_id}")
    return latest_run_id


def get_log_for_run(run_id: str) -> str:
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    jobs_url = f"{GITHUB_API}/repos/{GITHUB_REPO}/actions/runs/{run_id}/jobs"
    jobs_res = requests.get(jobs_url, headers=headers)

    if not jobs_res.ok:
        raise Exception(f"Failed to get jobs: {jobs_res.status_code} {jobs_res.text}")

    jobs = jobs_res.json().get("jobs", [])
    if not jobs:
        raise Exception("No jobs found in the workflow run.")

    log_url = f"{GITHUB_API}/repos/{GITHUB_REPO}/actions/jobs/{jobs[0]['id']}/logs"
    log_res = requests.get(log_url, headers=headers)

    if not log_res.ok:
        raise Exception(f"Failed to get logs: {log_res.status_code} {log_res.text}")

    return log_res.text


def extract_error_chunks(log_text: str) -> str:
    """
    Extract lines containing errors or key failures. Fallback to last 50 lines if nothing obvious.
    """
    lines = log_text.splitlines()
    error_lines = [line for line in lines if "error" in line.lower() or "::error::" in line.lower()]

    if error_lines:
        return "\n".join(error_lines[-100:])  # return last 100 error lines

    return "\n".join(lines[-50:])  # fallback


def main():
    parser = argparse.ArgumentParser(description="Summarize GitHub Actions logs with AI.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--run-id", type=str, help="GitHub Actions workflow run ID")
    group.add_argument("--latest", action="store_true", help="Use latest workflow run")
    parser.add_argument("--full", action="store_true", help="Send full log to LLM (instead of only errors)")

    args = parser.parse_args()

    # Determine which run ID to use
    run_id = args.run_id
    if args.latest:
        run_id = get_latest_run_id()

    print(" Fetching logs...")
    log_text = get_log_for_run(run_id)

    # Optional log preview
    print(" --- Log Preview (first 30 lines) ---")
    for line in log_text.splitlines()[:30]:
        print(line)
    print(" --- End Preview ---\n")

    print(" Summarizing logs with DeepSeek...\n")

    # Decide which part of log to summarize
    if args.full:
        summary = summarize_logs(log_text)
    else:
        summary = summarize_logs(extract_error_chunks(log_text))

    print("Summary:\n")
    print(summary)


if __name__ == "__main__":
    main()
