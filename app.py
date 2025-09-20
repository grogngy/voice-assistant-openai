"""
Voice Assistant OpenAI - Flask Application
A real-time voice and text chat application with OpenAI GPT integration.
"""

import os
import logging
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

# Configure logging
logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Ensure logs directory exists
os.makedirs('logs', exist_ok=True)


@app.route('/')
def index():
    """Main application page."""
    return render_template('index.html')


@app.route('/health')
def health_check():
    """Health check endpoint for monitoring."""
    return jsonify({
        'status': 'healthy',
        'service': 'voice-assistant-openai',
        'version': '1.0.0'
    })


@app.route('/config')
def config():
    """Return client configuration."""
    return jsonify({
        'openai_model': os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo'),
        'audio_sample_rate': int(os.getenv('AUDIO_SAMPLE_RATE', '16000')),
        'tts_language': os.getenv('TTS_LANGUAGE_CODE', 'en-US'),
        'stt_language': os.getenv('STT_LANGUAGE_CODE', 'en-US')
    })


@socketio.on('connect')
def handle_connect():
    """Handle client connection."""
    logger.info(f'Client connected: {request.sid}')
    emit('status', {'message': 'Connected to Voice Assistant'})


@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection."""
    logger.info(f'Client disconnected: {request.sid}')


@socketio.on('text_message')
def handle_text_message(data):
    """Handle text message from client."""
    logger.info(f'Received text message: {data.get("message", "")[:50]}...')
    
    # TODO: Integrate with OpenAI GPT
    response = {
        'message': f"Echo: {data.get('message', '')}",
        'type': 'text_response'
    }
    
    emit('ai_response', response)


@socketio.on('audio_data')
def handle_audio_data(data):
    """Handle audio data from client."""
    logger.info('Received audio data')
    
    # TODO: Integrate with Google Speech-to-Text
    # TODO: Process with OpenAI GPT
    # TODO: Convert response with Google Text-to-Speech
    
    response = {
        'message': 'Audio processing not yet implemented',
        'type': 'audio_response'
    }
    
    emit('ai_response', response)


if __name__ == '__main__':
    # Get configuration from environment
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', '8080'))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    logger.info(f'Starting Voice Assistant on {host}:{port}')
    logger.info(f'Debug mode: {debug}')
    logger.info(f'Environment: {os.getenv("FLASK_ENV", "development")}')
    
    # Run the application
    socketio.run(
        app,
        host=host,
        port=port,
        debug=debug,
        allow_unsafe_werkzeug=True
    )