import streamlit as st
import re
import subprocess
import shutil
import nltk

# Streamlit page config — must be first Streamlit command
st.set_page_config(page_title="Transcripto", layout="centered")

# Other imports (local modules)
from login import show_login_page
from home import load_summarizer, summarize_text
from model_guide import show_model_guide
from about import show_about
# from classifier import classify_topic
from logout import show_logout_page
from auth import cookies
from transcriber import transcribe_audio


# ------------------------------
# Initial Setup
# ------------------------------

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

# ------------------------------
# Auth Gating
# ------------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Auto-login if cookie exists
if cookies.get("user_email"):
    st.session_state.authenticated = True
    st.session_state.user_email = cookies.get("user_email")

if not st.session_state.authenticated:
    show_login_page()
else:
    st.sidebar.markdown(f"👤 Logged in as: `{st.session_state.user_email}`")
    page = st.sidebar.selectbox("📚 Navigate", ["Home", "Model Guide", "About", "Logout",])

    # ------------------------------
    # Helper: Extract YouTube Video ID
    # ------------------------------
    def extract_video_id(text):
        match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", text)
        return match.group(1) if match else None

    # ------------------------------
    # Download Audio using yt-dlp
    # ------------------------------
    def download_audio(video_id):
        url = f"https://www.youtube.com/watch?v={video_id}"
        output_path = f"{video_id}.mp3"

        if not shutil.which("yt-dlp"):
            raise RuntimeError("yt-dlp is not installed or not in PATH.")
        if not shutil.which("ffmpeg"):
            raise RuntimeError("FFmpeg is required but not found.")

        command = [
            "yt-dlp",
            "-x",
            "--audio-format", "mp3",
            "-o", output_path,
            url
        ]

        try:
            subprocess.run(command, check=True)
            return output_path
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"yt-dlp failed: {e}")

    # ------------------------------
    # Page Routing
    # ------------------------------
    if page == "Home":
        st.title("📝 Transcripto: YouTube or Transcript Summarizer")

        st.warning(
                    "⚠️ Note: Your app is running on CPU, so transcription may take longer than usual. "
                    "Please be patient while the audio is processed."
                )


        if "user_input" not in st.session_state:
            st.session_state.user_input = ""

        user_input = st.text_area("Paste YouTube URL or transcript", height=300, key="user_input")

        # if st.button("🧹 Clear Input"):
        #     st.session_state.user_input = ""
        #     st.rerun()

        model_choice = st.selectbox(
            "Choose a summarization model",
            ["facebook/bart-large-cnn", "t5-base", "google/pegasus-xsum"]
        )

        if st.button("Generate Summary") and user_input.strip():
            video_id = extract_video_id(user_input)

            try:
                if video_id:
                    st.info("🔄 Detected YouTube URL. Downloading audio...")
                    audio_path = download_audio(video_id)

                    st.info("🧠 Transcribing audio...")
                    transcript = transcribe_audio(audio_path)

                else:
                    st.info("📝 Detected raw transcript input.")
                    transcript = user_input

                # with st.spinner("🔍 Classifying topic..."):
                #     topic, confidence = classify_topic(transcript)

                # st.markdown(f"🏷️ **Detected Topic:** `{topic}` ({round(confidence * 100, 2)}%)")

                st.subheader("📄 Transcript Preview")
                st.text_area("Transcript", transcript[:3000], height=300)

                st.info(f"📦 Loading model: `{model_choice}`")
                summarizer = load_summarizer(model_choice)

                st.info("📝 Summarizing transcript...")
                summary = summarize_text(transcript, summarizer)

                st.success("✅ Summary generated successfully!")

                st.subheader("🧠 Summary")
                for i, sentence in enumerate(summary, 1):
                    st.markdown(f"**{i}.** {sentence}")
                    summary_text = "\n".join(summary)

                     
                st.markdown("## 📝 Share Your Feedback")
                form_url = "https://docs.google.com/forms/d/e/1FAIpQLSd1ZYSeE4dCMFHXQpHfZFITJmCmf-oVaEmpg0R7NPQF4Mnp_A/viewform?usp=dialog"
                st.markdown(f"[Click here to open the feedback form]({form_url})", unsafe_allow_html=True)
                    
                st.download_button(
                    label="📥 Download Summary as .txt",
                    data=summary_text,
                    file_name="summary.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error(f"⚠️ An error occurred: {e}")

    elif page == "Model Guide":
        show_model_guide()

    elif page == "About":
        show_about()

    elif page == "Logout":
        show_logout_page()   







