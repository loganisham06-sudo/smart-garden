import pytest
import sys
import os
import json

# Add parent directory to path to import the Flask app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from python_backend import app, garden_twin


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_get_garden_state(client):
    """Test that the /garden_state endpoint returns garden state."""
    response = client.get('/garden_state')
    assert response.status_code == 200
    data = response.get_json()
    assert 'bed_1' in data
    assert data['bed_1']['plant_type'] == 'Tomato'
    assert 'moisture_level' in data['bed_1']
    assert 'status' in data['bed_1']


def test_garden_state_initial_values():
    """Test that garden state has expected initial values."""
    assert garden_twin['bed_1']['plant_type'] == 'Tomato'
    assert garden_twin['bed_1']['threshold'] == 30.0
    assert isinstance(garden_twin['bed_1']['last_watered'], str)


def test_sensor_update_valid_data(client):
    """Test that the /sensor_update endpoint updates garden state with valid data."""
    update_data = {
        'bed_id': 'bed_1',
        'moisture': 55
    }
    response = client.post('/sensor_update', 
                          data=json.dumps(update_data),
                          content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'Twin Updated'
    assert data['current_state']['moisture_level'] == 55


def test_sensor_update_missing_data(client):
    """Test that the /sensor_update endpoint rejects incomplete data."""
    update_data = {
        'bed_id': 'bed_1'
    }
    response = client.post('/sensor_update',
                          data=json.dumps(update_data),
                          content_type='application/json')
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data


def test_sensor_update_invalid_moisture_range(client):
    """Test that the /sensor_update endpoint validates moisture range."""
    update_data = {
        'bed_id': 'bed_1',
        'moisture': 150  # Invalid: > 100
    }
    response = client.post('/sensor_update',
                          data=json.dumps(update_data),
                          content_type='application/json')
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data


def test_sensor_update_nonexistent_bed(client):
    """Test that the /sensor_update endpoint rejects nonexistent beds."""
    update_data = {
        'bed_id': 'bed_99',
        'moisture': 50
    }
    response = client.post('/sensor_update',
                          data=json.dumps(update_data),
                          content_type='application/json')
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data


def test_low_moisture_triggers_action(client):
    """Test that low moisture triggers action required status."""
    update_data = {
        'bed_id': 'bed_1',
        'moisture': 20  # Below threshold of 30
    }
    response = client.post('/sensor_update',
                          data=json.dumps(update_data),
                          content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    assert 'ACTION REQUIRED: Watering' in data['current_state']['status']
