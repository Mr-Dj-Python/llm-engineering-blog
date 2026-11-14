"""
reasoning_effort — the same model, fast vs thinking. (Newer models only.)

Run:  python 05_reasoning_effort.py
Look for: 'none' answers fast and may slip; 'high' thinks and is more reliable.
Note: if your model doesn't support reasoning_effort, it will error — that's expected;
      swap OPENAI_MODEL to a reasoning-capable model.
"""
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
if not os.getenv("OPENAI_API_KEY"):
    raise SystemExit("[skip] OPENAI_API_KEY not set")

client = OpenAI()
model = os.getenv("OPENAI_MODEL", "gpt-6-luna")
puzzle = [{"role": "user", "content":
    "You toss 2 coins. One is heads. Probability the other is tails? Answer with the number only."}]

for effort in ("none", "low", "high"):
    try:
        resp = client.chat.completions.create(model=model, messages=puzzle, reasoning_effort=effort)
        print(f"effort={effort:>4}: {resp.choices[0].message.content.strip()}")
    except Exception as e:
        print(f"effort={effort:>4}: [not supported by {model}] {e}")
