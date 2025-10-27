# transcriber.py
import os
import subprocess
from faster_whisper import WhisperModel

# ------------------------------
# Audio Preprocessing
# ------------------------------
def preprocess_audio(input_path, output_path="audio.wav"):
    """
    Convert audio to 16kHz mono WAV using ffmpeg.
    Fast Whisper prefers this format for accurate and faster transcription.
    """
    command = [
        "ffmpeg", "-y",        # Overwrite output if it exists
        "-i", input_path,      # Input file
        "-ar", "16000",        # Set sample rate to 16kHz
        "-ac", "1",            # Convert to mono
        output_path
    ]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return output_path

# ------------------------------
# Load Whisper Model
# ------------------------------
# Load once globally for caching in memory
# device="cuda" for GPU, "cpu" for CPU
# compute_type="float16" for faster GPU inference
model = WhisperModel("base", device="cuda", compute_type="float16")

# ------------------------------
# Transcription Function
# ------------------------------
def transcribe_audio(audio_path):
    """
    Preprocess audio and transcribe using Fast Whisper.
    Returns the full transcript as a string.
    """
    # 1. Preprocess audio
    wav_path = preprocess_audio(audio_path)

    # 2. Transcribe
    segments, info = model.transcribe(wav_path)

    # 3. Concatenate segments into full transcript
    transcript = " ".join([segment.text for segment in segments])

    # 4. Optional: Delete temporary WAV file
    os.remove(wav_path)

    return transcript
