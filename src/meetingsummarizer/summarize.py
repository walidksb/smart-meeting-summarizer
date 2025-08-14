from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from rich import print
from transformers import pipeline

from .config import settings
from .utils.chunking import split_by_words


@dataclass
class SummaryResult:
    bullets: List[str]
    merged_text: str


def load_summarizer(model_name: str | None = None):
    """
    Loads a local HF summarization pipeline. Defaults to BART CNN.
    """
    model = model_name or settings.summary_model
    print(f"[cyan]Loading summarization model:[/cyan] {model}")
    return pipeline("summarization", model=model, device=-1)


def summarize_long_text(
    text: str,
    summarizer=None,
    max_words_per_chunk: int = 800,
    max_length: int = 160,
    min_length: int = 60,
) -> SummaryResult:
    """
    Chunk the text and summarize each chunk; then merge into concise bullet points.
    """
    if summarizer is None:
        summarizer = load_summarizer()

    chunks = split_by_words(text, max_words=max_words_per_chunk)
    if not chunks:
        return SummaryResult(bullets=[], merged_text="")

    partials: List[str] = []
    for ch in chunks:
        out = summarizer(
            ch,
            max_length=max_length,
            min_length=min_length,
            do_sample=False,
        )[
            0
        ]["summary_text"]
        partials.append(out.strip())

    # Final pass: summarize the summaries for coherence
    merged_input = " ".join(partials)
    final = summarizer(
        merged_input,
        max_length=max_length,
        min_length=min_length,
        do_sample=False,
    )[0]["summary_text"].strip()

    # Turn into bullets heuristically
    bullets = [b.strip(" -•") for b in final.replace("\n", " ").split(". ") if b.strip()]
    return SummaryResult(bullets=bullets, merged_text=final)


def format_markdown_report(
    title: str,
    summary_bullets: List[str],
    decisions: List[str],
    action_items: List[Dict[str, str]],
) -> str:
    """Builds a clean Markdown meeting report."""
    md = [f"# {title}", "", "## Summary"]
    if summary_bullets:
        md.extend([f"- {b.rstrip('.')}" for b in summary_bullets])
    else:
        md.append("_No summary produced._")

    md.append("")
    md.append("## Key Decisions")
    if decisions:
        md.extend([f"- {d.rstrip('.')}" for d in decisions])
    else:
        md.append("_No explicit decisions found._")

    md.append("")
    md.append("## Action Items")
    if action_items:
        for a in action_items:
            who = a.get("assignee", "Unassigned")
            task = a.get("task", "—")
            due = a.get("due", "—")
            md.append(f"- **{who}** → {task} _(due: {due})_")
    else:
        md.append("_No action items detected._")

    md.append("")
    return "\n".join(md)
