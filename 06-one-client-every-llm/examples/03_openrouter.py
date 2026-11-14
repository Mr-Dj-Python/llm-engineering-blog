"""
OpenRouter — one key, many models behind a single OpenAI-compatible endpoint.

Run:  python 03_openrouter.py
Look for: a reply from a model you may not have a direct account with.
"""
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
key = os.getenv("OPENROUTER_API_KEY")
if not key:
    raise SystemExit("[skip] OPENROUTER_API_KEY not set")

openrouter = OpenAI(api_key=key, base_url="https://openrouter.ai/api/v1")
model = os.getenv("OPENROUTER_MODEL", "z-ai/glm-4.5")  # browse models at openrouter.ai

try:
    resp = openrouter.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": "Tell a short joke about databases."}],
    )
    print(f"=== OpenRouter ({model}) ===\n{resp.choices[0].message.content.strip()}")
except Exception as e:
    print(f"[error] {model}: {e}  (try a different model id from openrouter.ai)")
