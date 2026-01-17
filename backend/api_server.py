from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "API Server is running"})

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})

@app.route('/api/patients', methods=['GET'])
def get_patients():
    return jsonify({"patients": []})

@app.route('/api/devices', methods=['GET'])
def get_devices():
    return jsonify({"devices": []})

if __name__ == '__main__':
    app.run(debug=True)