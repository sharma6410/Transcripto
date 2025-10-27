# transcriber.py
import os
import subprocess
from faster_whisper import WhisperModel

# ------------------------------
# Audio Preprocessing
# ------------------------------
def preprocess_audio(input_path, output_path="audio.wav"):
    command = [
        "ffmpeg", "-y",
        "-i", input_path,
        "-ar", "16000",
        "-ac", "1",
        output_path
    ]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return output_path

# ------------------------------
# Lazy Model Loading
# ------------------------------
_model = None

def get_model():
    global _model
    if _model is None:
        _model = WhisperModel(
            "base",
            device="cpu",         # CPU-safe
            compute_type="float32" # Fully compatible
        )
    return _model

# ------------------------------
# Transcription Function
# ------------------------------
def transcribe_audio(audio_path):
    wav_path = preprocess_audio(audio_path)
    model = get_model()
    segments, _ = model.transcribe(wav_path)
    transcript = " ".join([segment.text for segment in segments])
    os.remove(wav_path)
    return transcript
