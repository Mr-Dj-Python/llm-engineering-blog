"""
NEGATIVE TESTS — the ways Claude prompt caching silently fails.
No error is raised in any of these; you only notice by watching the usage numbers.

Failure signatures:
  cache_write=0 AND cache_read=0  -> nothing cached at all
  cache_write>0 BUT cache_read=0  -> caching, but never reused (you pay the +25% write, get no benefit)

Run:  python 06_claude_caching_antipattern.py
Needs ANTHROPIC_API_KEY.
"""
import os, time
from dotenv import load_dotenv
import anthropic
from _sample import get_text

load_dotenv()
if not os.getenv("ANTHROPIC_API_KEY"):
    raise SystemExit("[skip] ANTHROPIC_API_KEY not set")

client = anthropic.Anthropic()
model = os.getenv("ANTHROPIC_MODEL", "claude-haiku-4-5")
BIG = get_text(unique=True)                 # ~12k tokens, well above the minimum
SMALL = "Short note, nowhere near the caching minimum for this model."

def run(label, system_builder):
    print(label)
    for q in ["Summary?", "Themes?"]:
        u = client.messages.create(model=model, max_tokens=32,
                                   system=system_builder(), messages=[{"role": "user", "content": q}]).usage
        print(f"   cache_write={u.cache_creation_input_tokens:>6}  cache_read={u.cache_read_input_tokens:>6}")

print(f"=== {model} ===")

# 1) Forgot cache_control entirely -> nothing is ever cached
run("1) No cache_control (block not marked):",
    lambda: [{"type": "text", "text": BIG}])

# 2) Marked block is below the model's minimum token count -> silently not cached
run("2) Block too small (below the model minimum):",
    lambda: [{"type": "text", "text": SMALL, "cache_control": {"type": "ephemeral"}}])

# 3) A changing value sits BEFORE the cached block -> prefix differs every call ->
#    it writes a new cache entry each time and never reads one back (pure waste)
run("3) Varying content before the cached block:",
    lambda: [{"type": "text", "text": f"[request {time.time()}]"},
             {"type": "text", "text": BIG, "cache_control": {"type": "ephemeral"}}])

# RIGHT) stable prefix, big block marked -> writes once, then reads (the win)
run("RIGHT) Stable prefix, big block cached:",
    lambda: [{"type": "text", "text": "Answer from the text."},
             {"type": "text", "text": BIG, "cache_control": {"type": "ephemeral"}}])
