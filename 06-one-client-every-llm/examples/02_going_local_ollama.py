"""
Going local — the same OpenAI client, pointed at Ollama on localhost.
Prereq: install Ollama, run `ollama serve`, then `ollama pull llama3.2`.

Run:  python 02_going_local_ollama.py
Look for: a reply from a model running on YOUR machine, same code shape as the cloud.
"""
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
ollama = OpenAI(api_key="ollama", base_url="http://localhost:11434/v1")  # key is ignored locally
model = os.getenv("OLLAMA_MODEL", "llama3.2")

try:
    resp = ollama.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": "In one sentence, what is an API?"}],
    )
    print(f"=== Ollama ({model}) ===\n{resp.choices[0].message.content.strip()}")
except Exception as e:
    print(f"[error] Is Ollama running and '{model}' pulled? → ollama serve / ollama pull {model}\n{e}")
