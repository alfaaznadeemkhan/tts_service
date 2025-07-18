import io
import os
import time
from concurrent.futures import ThreadPoolExecutor
import whisper
from flask import Flask, request, render_template, send_file, jsonify
from flask_cors import CORS
from gtts import gTTS
from pydub import AudioSegment

app = Flask(__name__)
CORS(app)
executor = ThreadPoolExecutor(max_workers=2)

# Preload whisper model (medium)
print("Loading Whisper model...")
model = whisper.load_model("medium")
print("Model loaded.")


# For Showing UI
@app.route("/")
def index():
    return render_template("index.html")


# Api for Text to speech
@app.route("/tts", methods=["POST"])
def text_to_speech():
    text = request.json.get("text")
    if not text:
        return jsonify({"error": "Text is required"}), 400

    try:
        # Convert text to speech
        tts = gTTS(text=text, lang="en")  # you can use 'hi' for Hindi, etc.

        # Save to in-memory buffer
        mp3_fp = io.BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)

        # Convert MP3 to WAV (optional, but better for web audio compatibility)
        audio = AudioSegment.from_file(mp3_fp, format="mp3")
        wav_fp = io.BytesIO()
        audio.export(wav_fp, format="wav")
        wav_fp.seek(0)

        return send_file(wav_fp, mimetype="audio/wav", as_attachment=False, download_name="output.wav")

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route("/transcribe", methods=["POST"])
def transcribe():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    future = executor.submit(process_audio_file, file)
    result = future.result()

    return jsonify(result)

def process_audio_file(file):
    import os, uuid

    start_time = time.time()

    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in [".mp3", ".wav", ".m4a"]:
        return {"error": "Unsupported file type"}

    # Save to temp file
    os.makedirs("temp", exist_ok=True)
    temp_path = f"temp/{uuid.uuid4()}{ext}"
    file.save(temp_path)

    try:
        result = model.transcribe(temp_path, fp16=False, verbose=False)
        elapsed = round(time.time() - start_time, 2)
        return {
            "text": result.get("text", ""),
            "language": result.get("language", "unknown"),
            "duration": elapsed
        }
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == "__main__":
    os.makedirs("temp", exist_ok=True)
    app.run(host="0.0.0.0", port=5050, debug=True)
