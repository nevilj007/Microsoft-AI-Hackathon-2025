import httpx
import json
import re

def clean_json(raw_response: str) -> str:
    """
    Extract the first valid JSON object from the raw LLM response.
    """
    match = re.search(r'{.*}', raw_response, re.DOTALL)
    return match.group(0) if match else raw_response.strip()

def parse_intent(natural_text: str) -> dict:
    prompt = f"""
You are an AI assistant converting user commands into structured GitHub Actions instructions.

Task: Convert the following command into a **strict JSON** object with:
- "workflow_file": the filename of the workflow (like "ci.yml", "build-and-push.yml" but if no filename specified then simply output" no filename specified")
- "ref": the Git branch name (like "main", "dev" but if no branch name specified then simply output" no branch name specified")

ONLY return a JSON object. No explanation, no markdown, no code fencing.

Command: {natural_text}
"""

    try:
        res = httpx.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "deepseek-coder:6.7b-instruct",
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )

        if res.status_code == 200:
            raw = res.json()["response"]
            print(f" Raw LLM response:\n{raw.strip()}")

            cleaned = clean_json(raw)
            return json.loads(cleaned)

        else:
            print(f" LLM error: {res.status_code} - {res.text}")
            return None

    except Exception as e:
        print(f" LLM request failed: {e}")
        return None
