from io import BytesIO

import soundfile as sf
from TTS.api import TTS

# Load the TTS model once
tts_model = TTS(model_name="tts_models/en/multi-dataset/tortoise-v2", progress_bar=True)

def synthesize_speech(text):
    # Generate speech (returns numpy audio array and sample rate)
    audio_array, sample_rate = tts_model.tts(text)

    # Save to in-memory WAV file
    buffer = BytesIO()
    sf.write(buffer, audio_array, sample_rate, format="WAV")
    buffer.seek(0)
    return buffer
