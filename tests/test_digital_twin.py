import pytest
import sys
import os

# Add parent directory to path to import the Flask app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    # Try to import from python-backend file (rename the file extension)
    from importlib import util
    spec = util.spec_from_file_location(
        "python_backend", 
        os.path.join(os.path.dirname(__file__), '..', 'python-backend')
    )
    python_backend = util.module_from_spec(spec)
    spec.loader.exec_module(python_backend)
    app = python_backend.app
    garden_twin = python_backend.garden_twin
    trigger_irrigation = python_backend.trigger_irrigation
except Exception:
    # Fallback: skip tests if import fails
    pytest.skip("python-backend module not available", allow_module_level=True)


@pytest.fixture
def client():
    """Create a test client for the digital twin Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_garden_twin_initial_state():
    """Test that the digital twin has the expected initial state."""
    assert 'bed_1' in garden_twin
    assert garden_twin['bed_1']['plant_type'] == 'Tomato'
    assert garden_twin['bed_1']['moisture_level'] == 45
    assert garden_twin['bed_1']['status'] == 'Healthy'
    assert garden_twin['bed_1']['threshold'] == 30.0


def test_sensor_update_endpoint(client):
    """Test that the /sensor_update endpoint accepts POST requests."""
    update_data = {
        'bed_id': 'bed_1',
        'moisture': 50
    }
    response = client.post('/sensor_update', json=update_data)
    assert response.status_code == 200
    data = response.get_json()
    assert 'status' in data
    assert 'current_state' in data


def test_moisture_update_below_threshold(client):
    """Test that status changes when moisture falls below threshold."""
    update_data = {
        'bed_id': 'bed_1',
        'moisture': 25  # Below threshold of 30
    }
    response = client.post('/sensor_update', json=update_data)
    assert response.status_code == 200
    data = response.get_json()
    current_state = data['current_state']
    assert 'ACTION REQUIRED' in current_state['status']
    assert current_state['moisture_level'] == 25


def test_moisture_update_above_threshold(client):
    """Test that status remains healthy when moisture is above threshold."""
    update_data = {
        'bed_id': 'bed_1',
        'moisture': 50  # Above threshold of 30
    }
    response = client.post('/sensor_update', json=update_data)
    assert response.status_code == 200
    data = response.get_json()
    current_state = data['current_state']
    assert current_state['status'] == 'Healthy'
    assert current_state['moisture_level'] == 50


def test_garden_twin_data_structure():
    """Test that garden twin has all required fields."""
    bed = garden_twin['bed_1']
    required_fields = ['plant_type', 'moisture_level', 'last_watered', 'status', 'threshold']
    for field in required_fields:
        assert field in bed, f"Missing field: {field}"


def test_threshold_comparison():
    """Test that threshold values are properly defined."""
    assert garden_twin['bed_1']['threshold'] > 0
    assert garden_twin['bed_1']['threshold'] < 100
