"""
One client, every model — the base_url trick.
Most providers expose OpenAI-compatible endpoints, so the SAME OpenAI client
reaches all of them; only base_url + key + model change.

Run:  python 01_one_client_many_models.py
Look for: each provider that has a key prints a joke; missing keys are skipped.
"""
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
PROMPT = [{"role": "user", "content": "Tell a short joke about APIs."}]

# (label, api_key, base_url, model)  -- base_url=None means default OpenAI endpoint
PROVIDERS = [
    ("OpenAI",    os.getenv("OPENAI_API_KEY"),    None,                                                        os.getenv("OPENAI_MODEL", "gpt-6-luna")),
    ("Anthropic", os.getenv("ANTHROPIC_API_KEY"), "https://api.anthropic.com/v1/",                             os.getenv("ANTHROPIC_MODEL", "claude-haiku-4-5")),
    ("Gemini",    os.getenv("GOOGLE_API_KEY"),    "https://generativelanguage.googleapis.com/v1beta/openai/",  os.getenv("GEMINI_MODEL", "gemini-2.0-flash")),
    ("Groq",      os.getenv("GROQ_API_KEY"),      "https://api.groq.com/openai/v1",                            os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")),
]

for label, key, base_url, model in PROVIDERS:
    if not key:
        print(f"[skip] {label}: no API key set")
        continue
    try:
        client = OpenAI(api_key=key, base_url=base_url)  # same class for everyone
        resp = client.chat.completions.create(model=model, messages=PROMPT)
        print(f"\n=== {label} ({model}) ===\n{resp.choices[0].message.content.strip()}")
    except Exception as e:
        print(f"[error] {label} ({model}): {e}")
