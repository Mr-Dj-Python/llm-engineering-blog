"""Shared helper: download a large public-domain text once to use as cached context.

Pass unique=True in a caching DEMO so each run starts with a cold cache (a per-process
marker is appended, making the context novel). Without it, a prior run's cache can bleed
into this one and hide the before/after contrast.
"""
import os, time, urllib.request

PATH = os.path.join(os.path.dirname(__file__), "hamlet.txt")
URL = "https://www.gutenberg.org/files/1524/1524-0.txt"
_NONCE = f"\n\n[demo run {time.time()}]"   # fixed once per process

def get_text(max_chars=40000, unique=False):
    if not os.path.exists(PATH):
        print("downloading sample text (hamlet.txt)...")
        urllib.request.urlretrieve(URL, PATH)
    with open(PATH, encoding="utf-8") as f:
        text = f.read()[:max_chars]
    return text + _NONCE if unique else text
