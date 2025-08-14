# Smart Meeting Summarizer (Open Source, English Only)

Free, local, privacy-friendly **meeting transcription + summarization**.

- **Transcription**: Faster-Whisper / Whisper (English)
- **Summarization**: `facebook/bart-large-cnn` (HF Transformers)
- **Outputs**: concise summary, key decisions, and action items
- **Interfaces**: CLI + Streamlit web app
- **Quality**: tests, CI, pre-commit (ruff + black), Dockerized

> No paid APIs or models. Fully open-source stack.

## ✨ Features
- Upload audio (mp3/wav) or paste transcript text
- Chunk-aware summarization for long meetings
- Heuristic **action item** extraction (assignments & due phrases)
- Export summaries as Markdown to `outputs/`
- Streamlit UI with download buttons

## 🧱 Architecture
Audio -> Faster-Whisper -> Transcript -> Chunking -> BART Summaries -> Merge -> Heuristic Action Extraction -> Markdown Report -> (CLI / Streamlit)

## 🚀 Quickstart
```bash
# 1) System dependency for audio decoding
sudo apt-get update && sudo apt-get install -y ffmpeg

# 2) Clone & install
git clone https://github.com/<your-username>/smart-meeting-summarizer.git
cd smart-meeting-summarizer
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt -r dev-requirements.txt
pre-commit install

# 3) Smoke test
pytest -q

# 4) CLI usage (with transcript file)
python -m meetingsummarizer.cli summarize --transcript data/sample/sample_transcript.txt \
  --out outputs/sample_report.md

# 5) Web app
streamlit run app/streamlit_app.py
