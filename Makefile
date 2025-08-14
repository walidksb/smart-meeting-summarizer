.PHONY: install dev lint format test run-app run-cli precommit docker

install:
	python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt

dev:
	pip install -r dev-requirements.txt && pre-commit install

lint:
	ruff check . && black --check .

format:
	black . && ruff check --fix .

test:
	pytest -q

run-app:
	streamlit run app/streamlit_app.py

run-cli:
	python -m meetingsummarizer.cli summarize --transcript data/sample/sample_transcript.txt --out outputs/sample_report.md

precommit:
	pre-commit run --all-files

docker:
	docker build -t smart-meeting-summarizer .
