from flask import Flask, request, send_file, render_template, redirect, url_for
from gtts import gTTS
import os
import uuid
import whisper
from pydub import AudioSegment

app = Flask(__name__)

AUDIO_DIR = "audio"
TRANSCRIPTS_DIR = "transcripts"
os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(TRANSCRIPTS_DIR, exist_ok=True)

model = whisper.load_model("base")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/tts", methods=["POST"])
def tts():
    text = request.form.get("text")
    lang = request.form.get("language")

    if not text or not lang:
        return "Text and language are required", 400

    filename = f"{uuid.uuid4()}.mp3"
    filepath = os.path.join(AUDIO_DIR, filename)
    gTTS(text=text, lang=lang).save(filepath)

    return render_template("result.html", audio_file=filename)

@app.route("/transcribe", methods=["POST"])
def transcribe():
    file = request.files.get("audio")
    if not file:
        return "No file uploaded", 400

    ext = os.path.splitext(file.filename)[1].lower()
    temp_path = os.path.join(AUDIO_DIR, f"{uuid.uuid4()}{ext}")
    file.save(temp_path)

    # Convert to wav if not already
    if ext != ".wav":
        sound = AudioSegment.from_file(temp_path)
        temp_path_wav = temp_path.replace(ext, ".wav")
        sound.export(temp_path_wav, format="wav")
        os.remove(temp_path)
        temp_path = temp_path_wav

    result = model.transcribe(temp_path)
    transcript = result.get("text", "")

    transcript_file = os.path.join(TRANSCRIPTS_DIR, f"{uuid.uuid4()}.txt")
    with open(transcript_file, "w", encoding="utf-8") as f:
        f.write(transcript)

    return render_template("result.html", transcript=transcript)

@app.route("/audio/<filename>")
def serve_audio(filename):
    return send_file(os.path.join(AUDIO_DIR, filename), mimetype="audio/mpeg")
