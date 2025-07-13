from flask import Flask, request, send_file, render_template, redirect, url_for
from gtts import gTTS
import uuid
import os

app = Flask(__name__)
AUDIO_DIR = "/tmp/audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text = request.form.get("text")
        if not text:
            return "Please enter some text!", 400

        filename = f"{uuid.uuid4()}.mp3"
        filepath = os.path.join(AUDIO_DIR, filename)

        try:
            tts = gTTS(text=text, lang="hi")
            tts.save(filepath)
            return send_file(filepath, mimetype="audio/mpeg", as_attachment=True, download_name="tts_output.mp3")
        except Exception as e:
            return f"Error: {e}", 500

    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
