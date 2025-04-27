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
'''import httpx
import json
import re
import time

def clean_json(raw_response: str) -> str:
    """
    Extract the first valid JSON object from the raw LLM response.
    """
    match = re.search(r'{.*}', raw_response, re.DOTALL)
    return match.group(0) if match else raw_response.strip()

import httpx
import time

def wait_for_deepseek_ready(retries=30, wait_seconds=5):
    """
    Smarter wait: First check Ollama server, then gently send a small prompt.
    """
    print("⏳ Waiting for Ollama server to become ready...")

    # Step 1: Check Ollama server is responding
    for attempt in range(10):
        try:
            res = httpx.head("http://localhost:11434", timeout=5)
            if res.status_code == 200:
                print("✅ Ollama server is up.")
                break
        except Exception as e:
            print(f"🔁 Ollama not ready yet: {e}")
        time.sleep(3)
    else:
        print("❌ Ollama server did not respond. Giving up.")
        return False

    # Step 2: Now check if DeepSeek model can respond
    print("⏳ Waiting for DeepSeek model to be loaded...")

    test_prompt = {
        "model": "deepseek-coder:6.7b-instruct",
        "prompt": "Say hello.",
        "stream": False
    }

    for attempt in range(retries):
        try:
            res = httpx.post("http://localhost:11434/api/generate", json=test_prompt, timeout=60)
            if res.status_code == 200:
                print("✅ DeepSeek responded! Model is ready.")
                return True
            else:
                print(f"🕒 DeepSeek not ready yet (HTTP {res.status_code}) - retry {attempt+1}/{retries}")
        except Exception as e:
            print(f"🔁 Waiting for DeepSeek: {e}")

        time.sleep(wait_seconds)

    print("❌ DeepSeek model did not respond after multiple retries.")
    return False


def parse_intent(natural_text: str) -> dict:
    """
    Send natural language command to DeepSeek and parse structured intent.
    """
    if not wait_for_deepseek_ready():
        print("❌ DeepSeek not ready, skipping LLM intent parsing.")
        return None

    prompt = f"""
You are an AI assistant converting user commands into structured GitHub Actions instructions.

Task: Convert the following command into a **strict JSON** object with:
- "workflow_file": the filename of the workflow (like "ci.yml", "build-and-push.yml")
- "ref": the Git branch name (like "main", "dev")

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
            timeout=120
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
        print(f"❌ LLM request failed: {e}")
        return None'''

