import os
import uuid

# from model_loader import whisper_model  # ✅ FIXED: import from shared moduleimport os
import uuid

# def transcribe_audio_file(file, allowed_exts=None):
#     if allowed_exts is None:
#         allowed_exts = [".mp3", ".wav", ".m4a", ".mp4"]
#
#     ext = os.path.splitext(file.filename)[1].lower()
#     if ext not in allowed_exts:
#         return {"error": f"Unsupported file type: {ext}"}
#
#     os.makedirs("temp", exist_ok=True)
#     temp_path = os.path.join("temp", f"{uuid.uuid4()}{ext}")
#     file.save(temp_path)
#
#     try:
#         result = whisper_model.transcribe(temp_path)
#         return {
#             "text": result.get("text", "").strip(),
#             "language": result.get("language", "unknown")
#         }
#     except Exception as e:
#         return {"error": str(e)}
#     finally:
#         if os.path.exists(temp_path):
#             os.remove(temp_path)





# def transcribe_audio_file(file, allowed_exts=None):
#     if allowed_exts is None:
#         allowed_exts = [".mp3", ".wav", ".m4a", ".mp4"]
#
#     # Validate extension
#     ext = os.path.splitext(file.filename)[1].lower()
#     if ext not in allowed_exts:
#         return {"error": f"Unsupported file type: {ext}"}
#
#     # Save uploaded file to a temporary path
#     os.makedirs("temp", exist_ok=True)
#     temp_path = os.path.join("temp", f"{uuid.uuid4()}{ext}")
#     file.save(temp_path)
#
#     try:
#         # Run transcription using preloaded model
#         result = whisper_model.transcribe(temp_path)
#
#         return {
#             "text": result.get("text", "").strip(),
#             "language": result.get("language", "unknown")
#         }
#
#     except Exception as e:
#         return {"error": str(e)}
#
#     finally:
#         # Clean up temp file
#         if os.path.exists(temp_path):
#             os.remove(temp_path)



import os
import uuid
from faster_whisper import WhisperModel

# Load model globally for faster performance
model_size = "medium"  # or "base", "small", "large-v2" based on RAM/CPU
whisper_model = WhisperModel(model_size, compute_type="int8", cpu_threads=4)

def transcribe_audio_file(file, allowed_exts=None):
    if allowed_exts is None:
        allowed_exts = [".mp3", ".wav", ".m4a"]

    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in allowed_exts:
        return {"error": "Unsupported file type"}

    os.makedirs("temp", exist_ok=True)
    temp_path = f"temp/{uuid.uuid4()}{ext}"
    file.save(temp_path)

    try:
        segments, info = whisper_model.transcribe(temp_path)
        transcription = " ".join(segment.text for segment in segments)

        return {
            "text": transcription.strip(),
            "language": info.language
        }
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

