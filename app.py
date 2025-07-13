from flask import Flask, request, send_file, jsonify
from gtts import gTTS
import uuid
import os

app = Flask(__name__)

AUDIO_DIR = "audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

@app.route("/tts", methods=["POST"])
def tts_hindi():
    data = request.get_json()
    text = data.get("text")

    if not text:
        return jsonify({"error": "Text is required"}), 400

    filename = f"output_{uuid.uuid4()}.mp3"
    filepath = os.path.join(AUDIO_DIR, filename)

    try:
        tts = gTTS(text=text, lang='hi')
        tts.save(filepath)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return send_file(filepath, mimetype="audio/mpeg")

@app.route("/")
def home():
    return jsonify({"message": "Hindi TTS API using gTTS is running."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)