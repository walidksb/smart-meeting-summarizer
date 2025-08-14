from __future__ import annotations

import argparse
from pathlib import Path

from rich import print

from .pipeline import run_from_audio, run_from_transcript


def save_text(out_path: Path, text: str):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(text, encoding="utf-8")
    print(f"[blue]Saved:[/blue] {out_path}")


def cmd_transcribe(args: argparse.Namespace):
    from .transcribe import transcribe_audio

    text = transcribe_audio(args.audio, model_size=args.model_size, language="en")
    if args.out:
        save_text(Path(args.out), text)
    else:
        print(text)


def cmd_summarize(args: argparse.Namespace):
    transcript = Path(args.transcript).read_text(encoding="utf-8")
    res = run_from_transcript(transcript, title=args.title, max_words_per_chunk=args.max_words)
    if args.out:
        save_text(Path(args.out), res.markdown)
    else:
        print(res.markdown)


def cmd_run(args: argparse.Namespace):
    res = run_from_audio(
        args.audio, title=args.title, language="en", max_words_per_chunk=args.max_words
    )
    if args.out:
        save_text(Path(args.out), res.markdown)
    else:
        print(res.markdown)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="smart-meeting-summarizer",
        description="Transcribe & summarize meetings (free, local).",
    )
    sub = p.add_subparsers(dest="command", required=True)

    p1 = sub.add_parser("transcribe", help="Audio -> transcript")
    p1.add_argument("--audio", required=True, help="Path to mp3/wav")
    p1.add_argument(
        "--model-size", default="base", help="Whisper size (tiny/base/small/medium/large-v3)"
    )
    p1.add_argument("--out", help="Output .txt path")
    p1.set_defaults(func=cmd_transcribe)

    p2 = sub.add_parser("summarize", help="Transcript -> Markdown report")
    p2.add_argument("--transcript", required=True, help="Path to .txt transcript")
    p2.add_argument("--title", default="Meeting Minutes")
    p2.add_argument("--max-words", type=int, default=800)
    p2.add_argument("--out", help="Output .md path")
    p2.set_defaults(func=cmd_summarize)

    p3 = sub.add_parser("run", help="Audio -> Markdown report")
    p3.add_argument("--audio", required=True, help="Path to mp3/wav")
    p3.add_argument("--title", default="Meeting Minutes")
    p3.add_argument("--max-words", type=int, default=800)
    p3.add_argument("--out", help="Output .md path")
    p3.set_defaults(func=cmd_run)

    return p


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
