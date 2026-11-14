"""Shared helper: download a large public-domain text once to use as cached context."""
import os, urllib.request

PATH = os.path.join(os.path.dirname(__file__), "hamlet.txt")
URL = "https://www.gutenberg.org/files/1524/1524-0.txt"

def get_text(max_chars=40000):
    if not os.path.exists(PATH):
        print("downloading sample text (hamlet.txt)...")
        urllib.request.urlretrieve(URL, PATH)
    with open(PATH, encoding="utf-8") as f:
        return f.read()[:max_chars]
