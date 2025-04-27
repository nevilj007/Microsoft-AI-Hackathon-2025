import httpx
from summarize_ci_logs import extract_error_chunks


def summarize_log_with_kernel(log_text: str):
    prompt = f"""
You are a DevOps AI assistant.

You are analyzing the following GitHub Actions build log. Perform these actions:

1. Summarize what happened during the build.
2. Identify any failure points or error messages.
3. Suggest specific, actionable fixes for the issues.
4. Remember to mention all the steps one by one to fix the issue so that next attempt will be successfull.
5. Recommend best practices if applicable.

Here is the log:
{extract_error_chunks(log_text)}
"""

    try:
        response = httpx.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "deepseek-coder:6.7b-instruct",
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )

        if response.status_code == 200:
            return response.json()["response"].strip()
        return f"[HTTP Error {response.status_code}] {response.text}"

    except Exception as e:
        return f"[Request Error] {str(e)}"
