from flask import Flask, jsonify, request
import datetime

app = Flask(__name__)

# Mock database representing the "Digital Twin" state
garden_twin = {
    "bed_1": {
        "plant_type": "Tomato",
        "moisture_level": 45,  # Percentage
        "last_watered": "2026-04-28 08:00",
        "status": "Healthy",
        "threshold": 30.0
    }
}

@app.route('/garden_state', methods=['GET'])
def get_garden_state():
    """Retrieve current garden state"""
    return jsonify(garden_twin), 200

@app.route('/sensor_update', methods=['POST'])
def update_twin():
    """Update the Digital Twin with sensor data"""
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        bed_id = data.get('bed_id')
        current_moisture = data.get('moisture')
        
        # Validate required fields
        if not bed_id or current_moisture is None:
            return jsonify({"error": "bed_id and moisture are required"}), 400
        
        # Check if bed exists
        if bed_id not in garden_twin:
            return jsonify({"error": f"Bed {bed_id} not found"}), 404
        
        # Validate moisture range
        if not (0 <= current_moisture <= 100):
            return jsonify({"error": "Moisture must be between 0 and 100"}), 400
        
        # Update the Digital Twin
        garden_twin[bed_id]['moisture_level'] = current_moisture
        garden_twin[bed_id]['last_watered'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # Self-Preservation Logic
        if current_moisture < garden_twin[bed_id]['threshold']:
            garden_twin[bed_id]['status'] = "ACTION REQUIRED: Watering"
            trigger_irrigation(bed_id)
        else:
            garden_twin[bed_id]['status'] = "Healthy"
            
        return jsonify({
            "status": "Twin Updated",
            "current_state": garden_twin[bed_id],
            "timestamp": datetime.datetime.now().isoformat()
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def trigger_irrigation(bed_id):
    """Trigger irrigation for a specific bed"""
    # In a real app, this sends an MQTT signal to the physical water valve
    print(f"SIGNAL SENT: Opening valve for {bed_id}")
    return True

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True)
