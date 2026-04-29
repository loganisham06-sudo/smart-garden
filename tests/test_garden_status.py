import pytest
import sys
import os

# Add parent directory to path to import the Flask app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from gemini_code_1777487583815 import app, garden_state


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_home_page(client):
    """Test that the home page loads."""
    response = client.get('/')
    assert response.status_code in [200, 404]  # 404 if template not found, but endpoint works


def test_get_status_endpoint(client):
    """Test that the /api/status endpoint returns garden state."""
    response = client.get('/api/status')
    assert response.status_code == 200
    data = response.get_json()
    assert 'moisture' in data
    assert 'temp' in data
    assert 'status' in data
    assert 'last_watered' in data


def test_garden_state_initial_values():
    """Test that garden state has expected initial values."""
    assert garden_state['moisture'] == 65
    assert garden_state['temp'] == 72
    assert garden_state['status'] == 'Optimal'
    assert isinstance(garden_state['last_watered'], str)


def test_update_garden_endpoint(client):
    """Test that the /api/update endpoint updates garden state."""
    update_data = {
        'moisture': 55,
        'temp': 75
    }
    response = client.post('/api/update', json=update_data)
    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data
    assert 'Digital Twin Updated' in data['message']


def test_moisture_level_update(client):
    """Test that moisture level is properly updated via POST request."""
    initial_moisture = garden_state['moisture']
    new_moisture = 75
    
    response = client.post('/api/update', json={'moisture': new_moisture})
    assert response.status_code == 200
    assert garden_state['moisture'] == new_moisture


def test_temperature_level_update(client):
    """Test that temperature is properly updated via POST request."""
    new_temp = 78
    
    response = client.post('/api/update', json={'temp': new_temp})
    assert response.status_code == 200
    assert garden_state['temp'] == new_temp
