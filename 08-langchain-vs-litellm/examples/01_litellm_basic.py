"""
LiteLLM — the thin unified call. One function, any provider, cost for free.
Switch provider by changing the model string (openai/..., anthropic/..., gemini/...).

Run:  python 01_litellm_basic.py
Look for: the reply plus total tokens and cost — no framework needed.
"""
import os
from dotenv import load_dotenv
from litellm import completion

load_dotenv()
model = os.getenv("LITELLM_MODEL", "openai/" + os.getenv("OPENAI_MODEL", "gpt-4.1-mini"))

resp = completion(model=model, messages=[{"role": "user", "content": "Tell a short joke about frameworks."}])
u = resp.usage
cost = (resp._hidden_params.get("response_cost") or 0) * 100

print(f"=== LiteLLM ({model}) ===")
print(resp.choices[0].message.content.strip(), "\n")
print(f"total tokens: {u.total_tokens}   cost: {cost:.4f} cents")
