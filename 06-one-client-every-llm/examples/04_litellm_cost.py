"""
LiteLLM — one function for any provider, with token + cost readout for free.

Run:  python 04_litellm_cost.py
Look for: the reply plus input/output tokens and the cost in cents.
"""
import os
from dotenv import load_dotenv
from litellm import completion

load_dotenv()
model = os.getenv("LITELLM_MODEL", "openai/" + os.getenv("OPENAI_MODEL", "gpt-6-luna"))

resp = completion(model=model, messages=[{"role": "user", "content": "Tell a short joke about caching."}])
u = resp.usage
cost = (resp._hidden_params.get("response_cost") or 0) * 100  # internal field; may be None on some versions

print(f"=== LiteLLM ({model}) ===\n{resp.choices[0].message.content.strip()}\n")
print(f"input tokens:  {u.prompt_tokens}")
print(f"output tokens: {u.completion_tokens}")
print(f"total tokens:  {u.total_tokens}")
print(f"cost:          {cost:.4f} cents")
