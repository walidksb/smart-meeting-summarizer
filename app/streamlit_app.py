from pathlib import Path

import streamlit as st

from src.meetingsummarizer.pipeline import run_from_audio, run_from_transcript

st.set_page_config(page_title="Smart Meeting Summarizer", page_icon="📝", layout="centered")

st.title("📝 Smart Meeting Summarizer")
st.caption("Free, local: Faster-Whisper + BART. Upload audio or paste transcript.")

tab1, tab2 = st.tabs(["Audio Upload", "Paste Transcript"])

with tab1:
    audio = st.file_uploader("Upload meeting audio (mp3/wav)", type=["mp3", "wav"])
    col1, col2 = st.columns(2)
    with col1:
        title = st.text_input("Report Title", value="Meeting Minutes")
    with col2:
        max_words = st.number_input(
            "Max words / chunk", min_value=300, max_value=1600, value=800, step=50
        )

    if st.button("Generate Report from Audio", disabled=audio is None):
        if audio:
            # Save temp file
            tmpdir = Path(".streamlit_tmp")
            tmpdir.mkdir(exist_ok=True)
            tmp_audio = tmpdir / audio.name
            tmp_audio.write_bytes(audio.read())

            with st.spinner("Transcribing and summarizing..."):
                res = run_from_audio(
                    str(tmp_audio), title=title, language="en", max_words_per_chunk=max_words
                )

            st.success("Done!")
            st.subheader("Preview")
            st.markdown(res.markdown)
            st.download_button(
                "Download Markdown", data=res.markdown, file_name="meeting_report.md"
            )


with tab2:
    title2 = st.text_input("Report Title ", value="Meeting Minutes (Transcript)")
    transcript_text = st.text_area(
        "Paste transcript text", height=260, placeholder="Paste your transcript here..."
    )
    max_words2 = st.number_input(
        "Max words / chunk ", min_value=300, max_value=1600, value=800, step=50, key="mw2"
    )

    if st.button("Generate Report from Transcript", disabled=not transcript_text.strip()):
        with st.spinner("Summarizing..."):
            res = run_from_transcript(transcript_text, title=title2, max_words_per_chunk=max_words2)
        st.success("Done!")
        st.subheader("Preview")
        st.markdown(res.markdown)
        st.download_button("Download Markdown", data=res.markdown, file_name="meeting_report.md")
