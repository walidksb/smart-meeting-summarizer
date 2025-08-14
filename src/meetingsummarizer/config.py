from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class Settings:
    transcribe_model_size: str = os.getenv("SMS_TRANSCRIBE_MODEL_SIZE", "base")
    summary_model: str = os.getenv("SMS_SUMMARY_MODEL", "facebook/bart-large-cnn")
    max_tokens_per_chunk: int = int(os.getenv("SMS_MAX_TOKENS_PER_CHUNK", "800"))


settings = Settings()
