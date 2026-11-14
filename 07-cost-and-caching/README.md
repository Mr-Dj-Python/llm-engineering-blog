# Stop paying for the same tokens twice

Cost + caching examples. The caching demos use a large text file (`hamlet.txt`) as the
static context — `_sample.py` downloads it once (git-ignored).

| # | File | Shows |
|---|------|-------|
| 01 | `examples/01_measure_cost.py` | measure token count + cost per call with LiteLLM |
| 02 | `examples/02_openai_caching.py` | OpenAI automatic caching — watch `cached` rise, cost drop |
| 03 | `examples/03_claude_caching.py` | Claude explicit caching — cache_write (prime +25%) then cache_read (10x cheaper) |
| 04 | `examples/04_reasoning_effort_cost.py` | reasoning effort as a cost lever |

Put run screenshots in `screenshots/`.

### Negative example
| # | File | Shows (anti-pattern) |
|---|------|---------------------|
| 05 | `examples/05_caching_antipattern.py` | prompt ordered wrong (variable first) → cache never hits; same run shows the fix |
