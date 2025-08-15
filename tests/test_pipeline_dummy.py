from meetingsummarizer.pipeline import run_from_transcript


def test_pipeline_from_transcript_runs():
    transcript = (
        "Walid: Let's finalize sprint goals. Rayan will prepare the API spec by Friday. "
        "Decision: we ship the beta to 10 users next week. Moh should write tests."
    )
    res = run_from_transcript(transcript, title="Test Meeting", max_words_per_chunk=200)
    assert "Summary" in res.markdown
    assert "Action Items" in res.markdown
