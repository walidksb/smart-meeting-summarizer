from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from rich import print

from .actions import extract_action_items, extract_decisions
from .config import settings
from .summarize import SummaryResult, format_markdown_report, summarize_long_text
from .transcribe import transcribe_audio


@dataclass
class RunResult:
    transcript: str
    summary: SummaryResult
    decisions: list[str]
    actions: list[dict]
    markdown: str


def run_from_audio(
    audio_path: str,
    title: str = "Meeting Minutes",
    language: Optional[str] = "en",
    max_words_per_chunk: int = 800,
) -> RunResult:
    print(f"[green]Transcribing audio:[/green] {audio_path}")
    transcript = transcribe_audio(
        audio_path, model_size=settings.transcribe_model_size, language=language
    )
    return run_from_transcript(transcript, title=title, max_words_per_chunk=max_words_per_chunk)


def run_from_transcript(
    transcript_text: str,
    title: str = "Meeting Minutes",
    max_words_per_chunk: int = 800,
) -> RunResult:
    print("[green]Summarizing transcript...[/green]")
    summary = summarize_long_text(
        transcript_text,
        summarizer=None,
        max_words_per_chunk=max_words_per_chunk,
    )
    decisions = extract_decisions(transcript_text + " " + summary.merged_text)
    actions = extract_action_items(transcript_text + " " + summary.merged_text)
    md = format_markdown_report(title, summary.bullets, decisions, actions)
    return RunResult(
        transcript=transcript_text,
        summary=summary,
        decisions=decisions,
        actions=actions,
        markdown=md,
    )
