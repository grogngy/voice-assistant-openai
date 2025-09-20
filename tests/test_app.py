"""
Test suite for Voice Assistant OpenAI application.
"""

import pytest
import json
from app import app, socketio


@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def socket_client():
    """Create a test client for SocketIO."""
    return socketio.test_client(app)


def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert data['service'] == 'voice-assistant-openai'
    assert 'version' in data


def test_index_page(client):
    """Test the main index page."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Voice Assistant' in response.data


def test_config_endpoint(client):
    """Test the configuration endpoint."""
    response = client.get('/config')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'openai_model' in data
    assert 'audio_sample_rate' in data
    assert 'tts_language' in data
    assert 'stt_language' in data


def test_socket_connection(socket_client):
    """Test WebSocket connection."""
    received = socket_client.get_received()
    assert len(received) > 0
    assert received[0]['name'] == 'status'


def test_text_message_handling(socket_client):
    """Test text message handling via WebSocket."""
    test_message = "Hello, assistant!"
    
    socket_client.emit('text_message', {'message': test_message})
    
    received = socket_client.get_received()
    # Should receive initial status + ai_response
    assert len(received) >= 2
    
    # Find the AI response
    ai_response = None
    for msg in received:
        if msg['name'] == 'ai_response':
            ai_response = msg
            break
    
    assert ai_response is not None
    assert 'message' in ai_response['args'][0]


def test_audio_data_handling(socket_client):
    """Test audio data handling via WebSocket."""
    fake_audio_data = b"fake_audio_data"
    
    socket_client.emit('audio_data', {'audio': fake_audio_data})
    
    received = socket_client.get_received()
    # Should receive initial status + ai_response
    assert len(received) >= 2
    
    # Find the AI response
    ai_response = None
    for msg in received:
        if msg['name'] == 'ai_response':
            ai_response = msg
            break
    
    assert ai_response is not None
    assert 'message' in ai_response['args'][0]


if __name__ == '__main__':
    pytest.main([__file__])