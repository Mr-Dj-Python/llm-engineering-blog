"""
Reasoning effort as a cost lever — more thinking = more tokens = more cost.

Run:  python 04_reasoning_effort_cost.py
Look for: higher effort -> more output tokens / higher cost on the same model.
Note: requires a reasoning-capable model; otherwise it reports 'not supported'.
"""
import os
from dotenv import load_dotenv
from litellm import completion

load_dotenv()
model = os.getenv("LITELLM_MODEL", "openai/" + os.getenv("OPENAI_MODEL", "gpt-6-luna"))
puzzle = [{"role": "user", "content": "A bat and ball cost $1.10. The bat costs $1 more than the ball. How much is the ball?"}]

for effort in ("low", "high"):
    try:
        r = completion(model=model, messages=puzzle, reasoning_effort=effort)
        u = r.usage
        cost = (r._hidden_params.get("response_cost") or 0) * 100
        print(f"effort={effort:>4}: out_tokens={u.completion_tokens:>5}  cost={cost:.4f}c  ->  {r.choices[0].message.content.strip()[:60]}")
    except Exception as e:
        print(f"effort={effort:>4}: [not supported by {model}] {e}")
