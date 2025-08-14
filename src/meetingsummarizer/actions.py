from __future__ import annotations

import re
from typing import Dict, List

ASSIGNEE_HINTS = r"(?:^|\b)([A-Z][a-zA-Z]+):?|(?:by|for)\s+([A-Z][a-zA-Z]+)\b"
DUE_HINTS = (
    r"\b(by|before|due)\s+"
    r"(?:EOD|end of day|tomorrow|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday|"
    r"next week|[A-Z][a-z]+\s+\d{1,2}|[0-9]{4}-[0-9]{2}-[0-9]{2})\b"
)


def extract_decisions(text: str) -> List[str]:
    """
    Very lightweight heuristic for key decisions.
    Looks for sentences containing 'decide/decision/approved/agree'.
    """
    sents = re.split(r"(?<=[.!?])\s+", text)
    keep = []
    for s in sents:
        low = s.lower()
        if any(k in low for k in ["decision", "decide", "decided", "approved", "agree", "agreed"]):
            keep.append(s.strip())
    return keep[:12]


def extract_action_items(text: str) -> List[Dict[str, str]]:
    """
    Heuristic action extraction:
      - Detects who (Name:) or patterns with 'will/should/must'
      - Detects due phrases ('by Monday', 'due 2025-08-20', etc.)
    """
    sents = re.split(r"(?<=[.!?])\s+", text)
    actions: List[Dict[str, str]] = []

    for s in sents:
        s_clean = s.strip()
        low = s_clean.lower()
        if not s_clean:
            continue

        # Must contain a commitment verb
        if not any(k in low for k in ["will", "should", "must", "to do", "need to", "assign"]):
            continue

        # Assignee guess
        assignee = None
        # Patterns like "Alice:", "Bob will", "by Carol"
        m_name = re.search(r"\b([A-Z][a-zA-Z]+)\b\s+(?:will|should|must|to)\b", s_clean)
        if m_name:
            assignee = m_name.group(1)
        else:
            m_hint = re.search(ASSIGNEE_HINTS, s_clean)
            if m_hint:
                assignee = next(g for g in m_hint.groups() if g)  # first non-None

        # Due guess
        due = None
        m_due = re.search(DUE_HINTS, s_clean, flags=re.IGNORECASE)
        if m_due:
            # capture the phrase after by/before/due
            due = s_clean[m_due.start() : m_due.end()]
            # keep only the date fragment after the keyword
            due = re.sub(r"^(by|before|due)\s+", "", due, flags=re.IGNORECASE)

        # Task is the sentence without the assignee label
        task = s_clean
        task = re.sub(r"^[A-Z][a-zA-Z]+:\s*", "", task)

        actions.append({"assignee": assignee or "Unassigned", "task": task, "due": due or "—"})

    # Deduplicate roughly
    seen = set()
    unique = []
    for a in actions:
        key = (a["assignee"], a["task"])
        if key not in seen:
            seen.add(key)
            unique.append(a)
    return unique[:30]
