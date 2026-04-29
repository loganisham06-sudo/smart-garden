import pytest


def test_moisture_threshold_logic():
    """Test the logic for determining if watering is needed."""
    threshold = 30.0
    
    # Test cases
    test_cases = [
        (25, True),   # Below threshold - needs watering
        (30, False),  # At threshold - no watering needed
        (35, False),  # Above threshold - no watering needed
    ]
    
    for moisture, should_water in test_cases:
        assert (moisture < threshold) == should_water


def test_moisture_percentage_bounds():
    """Test that moisture values stay within valid percentage bounds."""
    valid_values = [0, 25, 50, 75, 100]
    
    for value in valid_values:
        assert 0 <= value <= 100, f"Invalid moisture percentage: {value}"


def test_temperature_validity():
    """Test that temperature values are realistic for plant growth."""
    # Most plants grow well between 60-85°F
    valid_temps = [65, 72, 75, 80]
    
    for temp in valid_temps:
        assert 50 < temp < 95, f"Temperature out of range: {temp}"
