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
    """
    command = [
        "ffmpeg", "-y",        # Overwrite output if exists
        "-i", input_path,      # Input file
        "-ar", "16000",        # Sample rate 16kHz
        "-ac", "1",            # Mono
        output_path
    ]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return output_path

# ------------------------------
# Lazy Model Loading
# ------------------------------
_model = None

def get_model():
    """
    Load the Whisper model only when first needed.
    Uses CPU for environments without GPU.
    """
    global _model
    if _model is None:
        _model = WhisperModel(
            "base",
            device="cpu",            # Change to "cuda" if GPU is available
            compute_type="int8_float16"  # CPU-friendly and memory-efficient
        )
    return _model

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

    # 2. Get model (lazy load)
    model = get_model()

    # 3. Transcribe audio
    segments, _ = model.transcribe(wav_path)
    transcript = " ".join([segment.text for segment in segments])

    # 4. Clean up temporary WAV file
    os.remove(wav_path)

    return transcript
