from flask import Flask, request, send_file, render_template, jsonify
from gtts import gTTS
import os
import uuid
import whisper
from pydub import AudioSegment

app = Flask(__name__)
AUDIO_DIR = "audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

model = whisper.load_model("base")

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/tts", methods=["POST"])
def tts():
    try:
        data = request.get_json(force=True)
        text = data.get("text")
        if not text:
            return jsonify({"error": "Text is required"}), 400

        filepath = os.path.join(AUDIO_DIR, f"{uuid.uuid4()}.mp3")
        gTTS(text=text, lang="en").save(filepath)
        return send_file(filepath, mimetype="audio/mpeg")

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/transcribe", methods=["POST"])
def transcribe():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    ext = os.path.splitext(file.filename)[1].lower()
    temp_path = os.path.join(AUDIO_DIR, f"{uuid.uuid4()}{ext}")
    file.save(temp_path)

    if ext != ".wav":
        audio = AudioSegment.from_file(temp_path)
        temp_wav_path = temp_path.replace(ext, ".wav")
        audio.export(temp_wav_path, format="wav")
        os.remove(temp_path)
        temp_path = temp_wav_path

    result = model.transcribe(temp_path)
    return jsonify({"text": result["text"]})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
