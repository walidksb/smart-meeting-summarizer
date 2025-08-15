from src.meetingsummarizer.actions import extract_action_items, extract_decisions


def test_extract_decisions():
    text = "Decision: ship beta next week. We also agreed to update docs."
    dec = extract_decisions(text)
    assert any("Decision" in d or "agreed" in d.lower() for d in dec)


def test_extract_action_items():
    text = "Walid will prepare the API spec by Monday. Rayan should update the README."
    acts = extract_action_items(text)
    who = [a["assignee"] for a in acts]
    assert "Walid" in who or "Rayan" in who
    assert any("API spec" in a["task"] for a in acts)
