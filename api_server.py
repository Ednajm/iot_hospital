from flask import Flask, jsonify, request
import sys
sys.path.append('.')
from backend.database import HospitalDatabase

app = Flask(__name__)
db = HospitalDatabase()

@app.route('/')
def home():
    return jsonify({"message": "API Server is running"})

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "API Server is running"})

@app.route('/api/patients', methods=['GET'])
def get_patients():
    patient_id = request.args.get('patient_id')
    if patient_id:
        data = db.get_latest_patient_data(patient_id)
        return jsonify({"patient": data})
    stats = db.get_statistics()
    return jsonify({"total_records": stats.get('total_patient_records', 0)})

@app.route('/api/patients/<patient_id>', methods=['GET'])
def get_patient_by_id(patient_id):
    data = db.get_latest_patient_data(patient_id)
    return jsonify({"patient": data})

@app.route('/api/rooms', methods=['GET'])
def get_rooms():
    rooms = db.get_all_rooms_status()
    return jsonify({"rooms": rooms})
@app.route('/api/assets', methods=['GET'])
def get_assets():
    stats = db.get_statistics()
    return jsonify({"total_records": stats.get('total_asset_records', 0)})

@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    active_only = request.args.get('active', 'true').lower() == 'true'
    limit = request.args.get('limit', 50, type=int)
    if active_only:
        alerts = db.get_active_alerts(limit)
    else:
        alerts = db.get_all_alerts(limit)
    return jsonify({"alerts": alerts})
@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    stats = db.get_statistics()
    return jsonify({"statistics": stats})

if __name__ == '__main__':
    app.run(debug=True)