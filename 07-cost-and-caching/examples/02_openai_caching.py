"""
OpenAI automatic caching (via LiteLLM) — static content FIRST, variable LAST.
First call: cached=0. Second call: cached jumps, cost drops (same big prefix reused).

Run:  python 02_openai_caching.py
Look for: the 'cached' number going from 0 to large on the 2nd call.
"""
import os
from dotenv import load_dotenv
from litellm import completion
from _sample import get_text

load_dotenv()
BIG = get_text()
model = os.getenv("LITELLM_MODEL", "openai/" + os.getenv("OPENAI_MODEL", "gpt-6-luna"))

def ask(q):
    r = completion(model=model, messages=[
        {"role": "system", "content": "Answer using only the text below.\n\n" + BIG},  # STATIC first
        {"role": "user", "content": q},                                                # VARIABLE last
    ])
    u = r.usage
    cached = getattr(getattr(u, "prompt_tokens_details", None), "cached_tokens", 0) or 0
    cost = (r._hidden_params.get("response_cost") or 0) * 100
    print(f"input={u.prompt_tokens:>6}  cached={cached:>6}  cost={cost:.4f} cents")
    return r.choices[0].message.content

print(f"=== {model} ===")
ask("Give a one-line summary.")   # cached = 0
ask("Now list three themes.")     # cached jumps, cost drops
