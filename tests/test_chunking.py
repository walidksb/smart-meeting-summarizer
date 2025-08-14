from src.meetingsummarizer.utils.chunking import split_by_words


def test_split_by_words_basic():
    text = " ".join(["word"] * 100)
    chunks = split_by_words(text, max_words=30)
    assert len(chunks) == 4
    assert all(len(c.split()) <= 30 for c in chunks)
