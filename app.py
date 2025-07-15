from flask import Flask, request, render_template, send_file, jsonify
from gtts import gTTS
from faster_whisper import WhisperModel
from pydub import AudioSegment
import io
import tempfile
import os  # ✅ missing import

app = Flask(__name__)

# Load whisper model with low memory footprint
model = WhisperModel("base.en", compute_type="int8")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/tts", methods=["POST"])
def text_to_speech():
    text = request.json.get("text")
    if not text:
        return jsonify({"error": "Text is required"}), 400

    tts = gTTS(text=text, lang="en")
    mp3_buffer = io.BytesIO()
    tts.write_to_fp(mp3_buffer)
    mp3_buffer.seek(0)

    return send_file(mp3_buffer, mimetype="audio/mpeg", as_attachment=True, download_name="tts_output.mp3")

@app.route("/transcribe", methods=["POST"])
def transcribe():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No audio file uploaded"}), 400

    ext = os.path.splitext(file.filename)[1].lower()

    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        tmp_path = tmp.name
        file.save(tmp_path)

    try:
        if ext != ".wav":
            audio = AudioSegment.from_file(tmp_path)
            wav_path = tmp_path.replace(ext, ".wav")
            audio.export(wav_path, format="wav")
            os.remove(tmp_path)
            tmp_path = wav_path

        segments, _ = model.transcribe(tmp_path)
        transcript = " ".join([seg.text for seg in segments])

        return jsonify({"text": transcript})

    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)  # ✅ Removed trailing comma
