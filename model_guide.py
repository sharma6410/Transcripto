# model_guide.py

import streamlit as st

def show_model_guide():
    st.title("🧠 Model Guide: Choose the Right Summarizer")

    st.markdown("""
    Different transformer models have unique strengths. Here's a quick guide to help you choose:

    ### 🤖 BART (`facebook/bart-large-cnn`)
    - **Best for**: News articles, structured lectures, formal speech
    - **Pros**: Balanced summaries, good coherence
    - **Cons**: May miss nuance in casual or emotional speech

    ### 🧪 T5 (`t5-base`)
    - **Best for**: General-purpose summarization, flexible tasks
    - **Pros**: Lightweight, fast, adaptable
    - **Cons**: Can be vague or overly brief

    ### 🦄 Pegasus (`google/pegasus-xsum`)
    - **Best for**: Short, punchy summaries of conversational or informal content
    - **Pros**: Abstract and creative phrasing
    - **Cons**: May hallucinate or skip key details

    ---
    🔍 **Tip**: For technical explainers or tutorials, start with BART. For casual YouTube vlogs or storytelling, Pegasus might shine. T5 is a good fallback if you're unsure.
    """)

    st.info("You can switch models anytime from the dropdown on the Summarizer page.")
