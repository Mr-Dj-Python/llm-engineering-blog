"""
NEGATIVE EXAMPLE — why caching silently does nothing if you order the prompt wrong.

Caching keys off the PREFIX (the start of the prompt). The rule: static content FIRST,
variable content LAST. This script runs both ways so you can see the difference:

  WRONG: question first, big context last  -> prefix changes every call -> cached = 0
  RIGHT: big context first, question last   -> prefix is stable         -> cached jumps

Run:  python 05_caching_antipattern.py
Look for: 'cached' stays 0 in the WRONG block, and jumps in the RIGHT block — same data,
          same model, only the ORDER differs.
"""
import os
from dotenv import load_dotenv
from litellm import completion
from _sample import get_text

load_dotenv()
BIG = get_text()
model = os.getenv("LITELLM_MODEL", "openai/" + os.getenv("OPENAI_MODEL", "gpt-6-luna"))

def run(messages_builder, q):
    r = completion(model=model, messages=messages_builder(q))
    u = r.usage
    cached = getattr(getattr(u, "prompt_tokens_details", None), "cached_tokens", 0) or 0
    cost = (r._hidden_params.get("response_cost") or 0) * 100
    print(f"  input={u.prompt_tokens:>6}  cached={cached:>6}  cost={cost:.4f} cents")

# WRONG — variable (question) FIRST, static (context) LAST  -> prefix differs each call
def wrong(q):
    return [{"role": "user", "content": f"{q}\n\nUse this text:\n{BIG}"}]

# RIGHT — static (context) FIRST, variable (question) LAST  -> prefix is reused
def right(q):
    return [
        {"role": "system", "content": "Answer using only the text below.\n\n" + BIG},
        {"role": "user", "content": q},
    ]

print(f"=== {model} ===")
print("WRONG (variable first) — cache can't match:")
run(wrong, "Give a one-line summary.")
run(wrong, "Now list three themes.")      # cached still 0 — nothing reused

print("RIGHT (static first) — cache matches:")
run(right, "Give a one-line summary.")
run(right, "Now list three themes.")      # cached jumps — big prefix reused
