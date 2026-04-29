from flask import Flask, render_template, jsonify, request
import datetime

app = Flask(__name__)

# This is our "Digital Twin" Data Object
garden_state = {
    "moisture": 65,
    "last_watered": "10:30 AM",
    "status": "Optimal",
    "temp": 72
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/status')
def get_status():
    """Retrieve current garden status"""
    return jsonify(garden_state)

# Endpoint for your future IoT sensors to "talk" to the website
@app.route('/api/update', methods=['POST'])
def update_garden():
    """Update garden state with sensor data"""
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Validate and update moisture
        moisture = data.get('moisture')
        if moisture is not None:
            if not (0 <= moisture <= 100):
                return jsonify({"error": "Moisture must be between 0 and 100"}), 400
            garden_state['moisture'] = moisture
        
        # Validate and update temperature
        temp = data.get('temp')
        if temp is not None:
            if not (-50 <= temp <= 150):
                return jsonify({"error": "Temperature out of valid range"}), 400
            garden_state['temp'] = temp
        
        # Update last_watered timestamp if moisture was updated
        if moisture is not None:
            garden_state['last_watered'] = datetime.datetime.now().strftime("%I:%M %p")
        
        return jsonify({"message": "Digital Twin Updated!", "state": garden_state}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
