"""
Reasoning effort as a COST lever — across OpenAI, Claude, and Gemini through ONE LiteLLM
parameter. Higher effort = more thinking tokens = more cost, on the SAME model.
LiteLLM normalizes `reasoning_effort` to each provider's own thinking mechanism
(OpenAI reasoning_effort, Claude extended thinking, Gemini thinking budget).

Run:  python 08_reasoning_effort_providers.py
Look for: out_tokens and cost rising from low -> high effort for each provider.
"""
import os
from dotenv import load_dotenv
from litellm import completion

load_dotenv()
PUZZLE = [{"role": "user", "content":
    "A snail is at the bottom of a 10 m well. Each day it climbs 3 m, each night it "
    "slips back 2 m. How many days to reach the top? Think it through, then give the number."}]

PROVIDERS = [
    ("OpenAI", "gpt-5-mini",                   os.getenv("OPENAI_API_KEY")),
    ("Claude", "anthropic/claude-sonnet-5",    os.getenv("ANTHROPIC_API_KEY")),
    ("Gemini", "gemini/gemini-3.1-flash-lite", os.getenv("GEMINI_API_KEY")),
]

for label, model, key in PROVIDERS:
    if not key:
        print(f"{label}: [skip] no key"); continue
    print(f"{label}  ({model}):")
    for effort in ("low", "high"):
        try:
            r = completion(model=model, messages=PUZZLE, reasoning_effort=effort)
            u = r.usage
            cost = (r._hidden_params.get("response_cost") or 0) * 100
            print(f"   effort={effort:>4}   out_tokens={u.completion_tokens:>5}   cost={cost:.4f} cents")
        except Exception as e:
            print(f"   effort={effort:>4}   [not supported] {str(e)[:55]}")
