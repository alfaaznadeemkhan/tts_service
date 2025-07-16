# model_loader.py
import whisper

# Load the Whisper model only once here
whisper_model = whisper.load_model("medium")  # or "large"
