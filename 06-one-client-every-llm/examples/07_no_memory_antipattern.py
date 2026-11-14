"""
NEGATIVE EXAMPLE — a chatbot that forgets, and the one-line fix.

The model is stateless: it only knows what you send. If you DON'T carry the
conversation history, every turn starts from scratch and it can't remember anything.
This runs both ways with the same two messages so you can see it:

  WITHOUT memory: send only the latest message  -> it doesn't know your name
  WITH memory:    send the full history          -> it does

Run:  python 07_no_memory_antipattern.py
Needs OPENAI_API_KEY.
"""
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
if not os.getenv("OPENAI_API_KEY"):
    raise SystemExit("[skip] OPENAI_API_KEY not set")

client = OpenAI()
model = os.getenv("OPENAI_MODEL", "gpt-6-luna")

def ask(messages):
    return client.chat.completions.create(model=model, messages=messages).choices[0].message.content.strip()

print(f"=== {model} ===")

# --- WITHOUT memory: each call sends ONLY the current message ---
ask([{"role": "user", "content": "My name is Dhananjay."}])           # reply thrown away, not kept
answer = ask([{"role": "user", "content": "What's my name?"}])        # no history -> can't know
print(f"WITHOUT memory -> {answer}")

# --- WITH memory: send the whole conversation each turn ---
history = [{"role": "user", "content": "My name is Dhananjay."}]
history.append({"role": "assistant", "content": ask(history)})        # keep the reply
history.append({"role": "user", "content": "What's my name?"})        # append next turn
print(f"WITH memory    -> {ask(history)}")
