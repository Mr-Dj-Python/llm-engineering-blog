"""
Claude explicit caching — mark the big static block with cache_control.
First call: large cache_write (priming, +25%). Second call: large cache_read (10x cheaper).

Run:  python 03_claude_caching.py
Look for: cache_write large then ~0; cache_read 0 then large.
"""
import os
from dotenv import load_dotenv
import anthropic
from _sample import get_text

load_dotenv()
if not os.getenv("ANTHROPIC_API_KEY"):
    raise SystemExit("[skip] ANTHROPIC_API_KEY not set")

client = anthropic.Anthropic()
BIG = get_text(unique=True)
model = os.getenv("ANTHROPIC_MODEL", "claude-haiku-4-5")

def ask(q):
    resp = client.messages.create(
        model=model, max_tokens=256,
        system=[
            {"type": "text", "text": "Answer using only the provided text."},
            {"type": "text", "text": BIG, "cache_control": {"type": "ephemeral"}},  # cache this block
        ],
        messages=[{"role": "user", "content": q}],
    )
    u = resp.usage
    print(f"input={u.input_tokens:>5}  cache_write={u.cache_creation_input_tokens:>6}  cache_read={u.cache_read_input_tokens:>6}")
    return resp.content[0].text

print(f"=== {model} ===")
ask("Give a one-line summary.")   # cache_write large, cache_read 0
ask("Now list three themes.")     # cache_write 0, cache_read large
