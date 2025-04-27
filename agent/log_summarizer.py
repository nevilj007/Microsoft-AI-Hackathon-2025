import httpx

def summarize_logs(log_text: str) -> str:
    prompt = """
    You are a senior DevOps engineer reviewing a CI/CD build log from GitHub Actions.

    Your job is to:
    1. Summarize the log briefly.
    2. Identify any build/test/deployment errors.
    3. Suggest **specific** solutions or debug steps for each error found.
    4. Highlight any best practices that could help prevent this issue.

    Here is the log:
    {{input}}
        """
    try:
        response = httpx.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "deepseek-coder:6.7b-instruct",
                "prompt": prompt.replace("{{input}}", log_text),
                "stream": False
            },
            timeout=60.0  # Allow time for big logs
        )

        if response.status_code == 200:
            result = response.json()
            return result["response"]
        else:
            return f" Error {response.status_code}: {response.text}"

    except httpx.RequestError as e:
        return f" Request failed: {e}"
