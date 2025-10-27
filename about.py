import streamlit as st

def show_about():
    st.title("ℹ️ About Transcripto")

    st.markdown("""
    **Transcripto** is a smart, modular tool that transforms YouTube videos or raw transcripts into concise summaries using state-of-the-art NLP models.

    ### 🎯 What It Does
    - Extracts audio from YouTube links using `yt-dlp` and `ffmpeg`
    - Transcribes speech using OpenAI's Whisper
    - Summarizes content using transformer models like BART, T5, and Pegasus

    ### 🧠 Why It Matters
    - Skip long videos and get straight to the insights
    - Perfect for students, researchers, and content creators
    - Works with both YouTube URLs and manually pasted transcripts

    ### 🛠️ Built With
    - Python, Streamlit, HuggingFace Transformers
    - Whisper for transcription
    - Clean UI/UX with model guidance and download options

    ---
    👩‍💻 Created by Aditi — blending NLP, modular architecture, and local usability for real-world impact.
    """)
