"""
Measure what a call costs — you can't cut what you can't see.

Run:  python 01_measure_cost.py
Look for: input/output/total tokens and the cost in cents for one call.
"""
import os
from dotenv import load_dotenv
from litellm import completion

load_dotenv()
model = os.getenv("LITELLM_MODEL", "openai/" + os.getenv("OPENAI_MODEL", "gpt-4.1-mini"))

resp = completion(model=model, messages=[{"role": "user", "content": "Explain prompt caching in 2 sentences."}])
u = resp.usage
cost = (resp._hidden_params.get("response_cost") or 0) * 100

print(f"=== {model} ===")
print(resp.choices[0].message.content.strip(), "\n")
print(f"input={u.prompt_tokens}  output={u.completion_tokens}  total={u.total_tokens}  cost={cost:.4f} cents")
