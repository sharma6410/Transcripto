# transcriber.py
import subprocess
import os
import whisper
import torch
import streamlit as st

@st.cache_resource
def load_whisper_model():
    """Load Whisper model once and move to GPU if available."""
    model = whisper.load_model("base")
    if torch.cuda.is_available():
        model = model.to("cuda")
    return model

def preprocess_audio(input_path, output_path="audio.wav"):
    """Convert audio to 16kHz mono WAV using ffmpeg."""
    command = [
        "ffmpeg", "-y",
        "-i", input_path,
        "-ar", "16000",
        "-ac", "1",
        output_path
    ]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return output_path

def transcribe_audio(audio_path):
    """Preprocess audio and transcribe using Whisper."""
    model = load_whisper_model()
    wav_path = preprocess_audio(audio_path)
    result = model.transcribe(wav_path)
    os.remove(wav_path)  # optional cleanup
    return result["text"]
