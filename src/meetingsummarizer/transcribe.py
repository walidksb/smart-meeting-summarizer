from __future__ import annotations

from typing import Optional

from rich import print

try:
    from faster_whisper import WhisperModel
except Exception:  # pragma: no cover
    WhisperModel = None  # type: ignore


def transcribe_audio(
    audio_path: str, model_size: str = "base", language: Optional[str] = "en"
) -> str:
    """Transcribe English audio using Faster-Whisper. Requires system ffmpeg."""
    if WhisperModel is None:
        raise RuntimeError("faster-whisper is not installed. `pip install faster-whisper`.")

    model = WhisperModel(model_size, compute_type="auto")
    segments, info = model.transcribe(audio_path, language=language, beam_size=5)

    transcript_parts = [seg.text.strip() for seg in segments if seg.text.strip()]
    text = " ".join(transcript_parts)

    print(
        f"[green]Detected language:[/green] {info.language} | prob={info.language_probability:.2f}"
    )
    return text.strip()
