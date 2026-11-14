"""
LangChain — the orchestration framework. The basic model call is tiny, but LangChain
exists for chains / agents / RAG / memory on top of it.

Run:  python 02_langchain_basic.py
Look for: the reply via ChatOpenAI.invoke — the same model call, inside a framework.
"""
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()
if not os.getenv("OPENAI_API_KEY"):
    raise SystemExit("[skip] OPENAI_API_KEY not set")

model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
llm = ChatOpenAI(model=model)
response = llm.invoke([{"role": "user", "content": "Tell a short joke about frameworks."}])

print(f"=== LangChain ChatOpenAI ({model}) ===")
print(response.content.strip())
print("\n(LangChain's value isn't this call — it's chains, agents, RAG, and memory built around it.)")
