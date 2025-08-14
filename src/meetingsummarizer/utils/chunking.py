from __future__ import annotations

from typing import List


def split_by_words(text: str, max_words: int = 800) -> List[str]:
    words = text.split()
    chunks = [" ".join(words[i : i + max_words]) for i in range(0, len(words), max_words)]
    return [c for c in chunks if c.strip()]
