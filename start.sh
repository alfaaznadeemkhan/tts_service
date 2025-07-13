#!/bin/bash

echo "[INFO] Preloading Coqui TTS model..."
python3 -c "from TTS.api import TTS; TTS(model_name='tts_models/multilingual/multi-dataset/xtts_v2')"

echo "[INFO] Starting Flask app..."
python3 app.py
