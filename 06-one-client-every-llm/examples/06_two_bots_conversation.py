"""
The messages-list pattern — the foundation of every chatbot and multi-agent setup.
Two bots talk to each other: one snarky (GPT), one polite (Claude). Each turn rebuilds
the messages list from the running history, so each bot "remembers" the whole exchange.

Run:  python 06_two_bots_conversation.py
Look for: a rude bot failing to rattle a polite one over 5 rounds.
Needs OPENAI_API_KEY and ANTHROPIC_API_KEY.
"""
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
if not (os.getenv("OPENAI_API_KEY") and os.getenv("ANTHROPIC_API_KEY")):
    raise SystemExit("[skip] needs both OPENAI_API_KEY and ANTHROPIC_API_KEY")

openai = OpenAI()
anthropic = OpenAI(api_key=os.getenv("ANTHROPIC_API_KEY"), base_url="https://api.anthropic.com/v1/")

gpt_model = os.getenv("OPENAI_MODEL", "gpt-6-luna")
claude_model = os.getenv("ANTHROPIC_MODEL", "claude-haiku-4-5")

gpt_system = "You are argumentative and snarky; you disagree with everything, briefly."
claude_system = "You are polite and courteous; you try to find common ground, briefly."

gpt_messages = ["Hi there"]
claude_messages = ["Hi"]

def call_gpt():
    msgs = [{"role": "system", "content": gpt_system}]
    for g, c in zip(gpt_messages, claude_messages):
        msgs.append({"role": "assistant", "content": g})
        msgs.append({"role": "user", "content": c})
    return openai.chat.completions.create(model=gpt_model, messages=msgs).choices[0].message.content

def call_claude():
    msgs = [{"role": "system", "content": claude_system}]
    for g, c in zip(gpt_messages, claude_messages):
        msgs.append({"role": "user", "content": g})
        msgs.append({"role": "assistant", "content": c})
    msgs.append({"role": "user", "content": gpt_messages[-1]})
    return anthropic.chat.completions.create(model=claude_model, messages=msgs).choices[0].message.content

print(f"GPT:    {gpt_messages[0]}")
print(f"Claude: {claude_messages[0]}")
for _ in range(5):
    g = call_gpt();   print(f"\nGPT:    {g.strip()}");   gpt_messages.append(g)
    c = call_claude(); print(f"Claude: {c.strip()}");    claude_messages.append(c)
