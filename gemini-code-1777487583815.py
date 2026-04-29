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
    return jsonify(garden_state)

# Endpoint for your future IoT sensors to "talk" to the website
@app.route('/api/update', methods=['POST'])
def update_garden():
    data = request.json
    garden_state['moisture'] = data.get('moisture', garden_state['moisture'])
    garden_state['temp'] = data.get('temp', garden_state['temp'])
    return jsonify({"message": "Digital Twin Updated!"})

if __name__ == '__main__':
    app.run(debug=True)