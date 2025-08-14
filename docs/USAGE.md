# Usage

## CLI
```bash
python -m meetingsummarizer.cli transcribe --audio /path/to/audio.mp3 --out outputs/transcript.txt
python -m meetingsummarizer.cli summarize --transcript outputs/transcript.txt --out outputs/report.md
# One-shot (audio -> report)
python -m meetingsummarizer.cli run --audio /path/to/audio.mp3 --out outputs/report.md
