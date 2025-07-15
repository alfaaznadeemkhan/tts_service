from flask import Flask, request, render_template, send_file, jsonify
from gtts import gTTS
from faster_whisper import WhisperModel
from pydub import AudioSegment
import os, uuid

app = Flask(__name__)

AUDIO_DIR = "audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

model = WhisperModel("base.en", compute_type="int8")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/tts", methods=["POST"])
def text_to_speech():
    text = request.json.get("text")
    if not text:
        return jsonify({"error": "Text is required"}), 400

    filename = f"{uuid.uuid4()}.mp3"
    filepath = os.path.join(AUDIO_DIR, filename)
    gTTS(text=text, lang="en").save(filepath)

    return send_file(filepath, mimetype="audio/mpeg")

@app.route("/transcribe", methods=["POST"])
def transcribe():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No audio file uploaded"}), 400

    ext = os.path.splitext(file.filename)[1].lower()
    filepath = os.path.join(AUDIO_DIR, f"{uuid.uuid4()}{ext}")
    file.save(filepath)

    if ext != ".wav":
        audio = AudioSegment.from_file(filepath)
        wav_path = filepath.replace(ext, ".wav")
        audio.export(wav_path, format="wav")
        os.remove(filepath)
        filepath = wav_path

    segments, _ = model.transcribe(filepath)
    transcript = " ".join([seg.text for seg in segments])

    return jsonify({"text": transcript})

@app.route("/audio/<filename>")
def serve_audio(filename):
    return send_file(os.path.join(AUDIO_DIR, filename))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)

