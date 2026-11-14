# LLM Engineering — blog examples

Runnable code accompanying my blog series on working with LLM APIs. Each folder maps
to one post; each script in `examples/` is a single, standalone example you can run and
read on its own. `screenshots/` holds the output captures used in the posts.

## Posts

| Folder | Post |
|---|---|
| `06-one-client-every-llm/` | One client, every LLM |
| `07-cost-and-caching/` | Stop paying for the same tokens twice |
| `08-langchain-vs-litellm/` | LangChain or LiteLLM? |

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # then fill in the keys you have
```

Every script loads `.env` and **skips any provider whose key is missing**, so you can run
with just one key. Model names default to current ones but are overridable in `.env` —
set them to models you actually have access to (provider model names change often).

## Running an example

```bash
python 06-one-client-every-llm/examples/01_one_client_many_models.py
```

> Note: model IDs move. If a script reports an unknown model, set the matching
> `*_MODEL` variable in `.env` to a current model from that provider.
