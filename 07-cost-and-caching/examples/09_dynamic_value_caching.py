"""
Does caching work when the prompt ends with a DYNAMIC value? Yes — if the dynamic part
is LAST, the static prefix is identical across calls and caches; only the tail is new.

Proven across all three vendors with a DIFFERENT dynamic tail on each call:
  OpenAI  - automatic prefix caching (deterministic)
  Claude  - explicit cache_control on the static block (deterministic)
  Gemini  - implicit caching (best-effort) -> averaged over 4 runs

Run:  python 09_dynamic_value_caching.py
"""
import os, time
from dotenv import load_dotenv
from litellm import completion
import anthropic
from _sample import get_text

load_dotenv()
BASE = get_text()                      # static document
TAILS = ["Summarize the text in one line.", "List three themes from the text."]
STATIC = "Answer using only the text below.\n\n"

def cost_of(r): return (r._hidden_params.get("response_cost") or 0) * 100
def cached_of(r):
    d = getattr(r.usage, "prompt_tokens_details", None)
    return getattr(d, "cached_tokens", 0) or 0

# ---- OpenAI (deterministic) ----
if os.getenv("OPENAI_API_KEY"):
    model = "openai/" + os.getenv("OPENAI_MODEL", "gpt-6-luna")
    big = BASE + f"\n[run {time.time()}]"
    print(f"OpenAI  ({model}):")
    for i, tail in enumerate(TAILS, 1):
        r = completion(model=model, messages=[{"role":"system","content":STATIC+big},
                                              {"role":"user","content":f"[request {i}] {tail}"}])
        print(f"   call {i}  dynamic=\"{tail[:26]}...\"  cached={cached_of(r):>6}  cost={cost_of(r):.4f} cents")

# ---- Claude (deterministic, explicit) ----
if os.getenv("ANTHROPIC_API_KEY"):
    c = anthropic.Anthropic(); model = os.getenv("ANTHROPIC_MODEL", "claude-haiku-4-5")
    big = BASE + f"\n[run {time.time()}]"
    print(f"Claude  ({model}):")
    for i, tail in enumerate(TAILS, 1):
        u = c.messages.create(model=model, max_tokens=48, system=[
            {"type":"text","text":"Answer using only the provided text."},
            {"type":"text","text":big,"cache_control":{"type":"ephemeral"}},
        ], messages=[{"role":"user","content":f"[request {i}] {tail}"}]).usage
        print(f"   call {i}  dynamic=\"{tail[:26]}...\"  cache_read={u.cache_read_input_tokens:>6}")

# ---- Gemini (implicit, best-effort) -> average call-2 cache over 4 runs ----
if os.getenv("GEMINI_API_KEY"):
    model = "gemini/gemini-3.1-flash-lite"
    print(f"Gemini  ({model})  — call 2 cache over 4 runs:")
    hits = []
    for run in range(1, 5):
        big = BASE + f"\n[run {run} {time.time()}]"   # fresh cold context each run
        c2 = None
        for i, tail in enumerate(TAILS, 1):
            for a in range(6):
                try:
                    r = completion(model=model, timeout=40, messages=[
                        {"role":"system","content":STATIC+big},
                        {"role":"user","content":f"[request {i}] {tail}"}])
                    if i == 2: c2 = cached_of(r)
                    break
                except Exception as e:
                    if "503" in str(e) or "UNAVAILABLE" in str(e): time.sleep(5); continue
                    raise
        hits.append(c2 or 0)
        print(f"   run {run}  call-2 cached={c2:>6}")
        time.sleep(2)
    print(f"   AVERAGE call-2 cached over 4 runs = {sum(hits)/len(hits):.0f} tokens")
