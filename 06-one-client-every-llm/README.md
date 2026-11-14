# One client, every LLM

Examples for the post. Run any file directly; each skips providers whose key is missing.

| # | File | Shows |
|---|------|-------|
| 01 | `examples/01_one_client_many_models.py` | one OpenAI client → OpenAI, Anthropic, Gemini, Groq via `base_url` |
| 02 | `examples/02_going_local_ollama.py` | the same client pointed at a local Ollama model |
| 03 | `examples/03_openrouter.py` | one key, many models through OpenRouter |
| 04 | `examples/04_litellm_cost.py` | one function for any provider + token/cost readout |
| 05 | `examples/05_reasoning_effort.py` | the `reasoning_effort` dial (none/low/high) |
| 06 | `examples/06_two_bots_conversation.py` | the messages-list pattern: a snarky bot vs a polite bot |

Put run screenshots in `screenshots/` (e.g. `01_one_client.png`).

### Negative example
| # | File | Shows (anti-pattern) |
|---|------|---------------------|
| 07 | `examples/07_no_memory_antipattern.py` | no conversation history → the bot forgets; same run shows the fix |
