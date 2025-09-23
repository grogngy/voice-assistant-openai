

# --- Dependency check block ---
missing = []
try:
    import flask
except ImportError:
    missing.append('flask')
try:
    import flask_cors
except ImportError:
    missing.append('flask-cors')
try:
    import dotenv
except ImportError:
    missing.append('python-dotenv')
if missing:
    print("\n[ERROR] Required packages missing: {}".format(", ".join(missing)))
    print("Please run: pip install -r requirements.txt or install the missing packages in your environment.")
    exit(1)

import base64
import os
import json
from flask import Flask, render_template, request
from worker import speech_to_text, text_to_speech, openai_process_message
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/speech-to-text', methods=['POST'])
def speech_to_text_route():
    if 'audio' not in request.files:
        print("[STT] No audio file provided in request.")
        return {"error": "No audio file provided"}, 400
    audio = request.files['audio']
    audio_path = "temp_audio.webm"
    audio.save(audio_path)
    file_size = os.path.getsize(audio_path)
    print(f"[STT] Received audio file: {audio_path}, size: {file_size} bytes")
    text = speech_to_text(audio_path)
    print(f"[STT] Transcript: '{text}'")
    os.remove(audio_path)
    return {"text": text}

@app.route('/text-to-speech', methods=['POST'])
def text_to_speech_route():
    data = request.get_json()
    text = data.get("text", "")
    voice = data.get("voice", "")
    print(f"Received text for TTS: {text}")
    print(f"Requested voice: {voice}")
    if not text or text.strip() == "":
        print("TTS error: Empty text received.")
        return {"audio": "", "error": "No text provided for TTS."}, 400
    # Truncate text to 1000 characters for TTS safety
    if len(text) > 1000:
        print(f"TTS input text too long ({len(text)} chars), truncating to 1000.")
        text = text[:1000]
    output_path = "output.mp3"
    try:
        text_to_speech(text, output_path, voice)
        if not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
            print("TTS output file missing or empty!")
            return {"audio": ""}, 500
        with open(output_path, "rb") as audio_file:
            audio_base64 = base64.b64encode(audio_file.read()).decode("utf-8")
        os.remove(output_path)
        return {"audio": audio_base64}
    except Exception as e:
        import traceback
        print(f"TTS error: {e}")
        traceback.print_exc()
        return {"audio": "", "error": str(e)}, 500

@app.route('/process-message', methods=['POST'])
def process_message_route():
    data = request.get_json()
    user_message = data.get("userMessage", "")
    response_text = openai_process_message(user_message)
    return {"genaiResponseText": response_text}

# ...existing code...


if __name__ == "__main__":
    import sys
    port = int(os.environ.get("PORT", 8080))
    use_ssl = os.environ.get("USE_SSL", "0") == "1"
    ssl_ctx = (r'certs/cert.pem', r'certs/key.pem') if use_ssl else None
    app.run(
        port=port,
        host='0.0.0.0',
        ssl_context=ssl_ctx
    )
# ...existing code...
