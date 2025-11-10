from flask import Flask, render_template, jsonify
from flask_cors import CORS
import random
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for API requests

# Mock data generators for demo purposes
def generate_patient_data():
    """Generate mock patient monitoring data"""
    return {
        'total': 5000,
        'critical': random.randint(8, 15),
        'patients': [
            {
                'id': f'P{1000 + i}',
                'name': ['Mario Rossi', 'Luigi Bianchi', 'Anna Verdi', 'Paolo Neri', 'Sara Gialli', 
                         'Marco Blu', 'Giulia Rosa', 'Andrea Viola', 'Elena Marrone', 'Simone Grigio'][i],
                'heartRate': random.randint(60, 120),
                'temperature': round(random.uniform(36.0, 38.5), 1),
                'spo2': random.randint(90, 100),
                'status': 'Alert' if random.random() > 0.7 else 'Normal'
            }
            for i in range(10)
        ],
        'timeSeries': {
            'labels': [f'{i:02d}:00' for i in range(24)],
            'heartRate': [random.randint(65, 95) for _ in range(24)],
            'spo2': [random.randint(94, 99) for _ in range(24)],
            'temperature': [round(random.uniform(36.3, 37.2), 1) for _ in range(24)]
        }
    }

def generate_room_data():
    """Generate mock room environmental data"""
    room_count = 5
    return {
        'total': 500,
        'occupied': random.randint(400, 450),
        'environmental': {
            'labels': [f'Room{i+1}' for i in range(room_count)],
            'temperature': [round(random.uniform(20.0, 26.0), 1) for _ in range(room_count)],
            'humidity': [random.randint(40, 65) for _ in range(room_count)],
            'co2': [random.randint(400, 800) for _ in range(room_count)]
        }
    }

def generate_asset_data():
    """Generate mock asset tracking data"""
    active = random.randint(165, 180)
    standby = random.randint(10, 20)
    maintenance = 199 - active - standby
    
    return {
        'total': 199,
        'active': active,
        'statusBreakdown': {
            'active': active,
            'standby': standby,
            'maintenance': maintenance
        }
    }

def generate_alerts():
    """Generate mock active alerts"""
    alert_templates = [
        {'title': 'Paziente {id} - Battito Anomalo', 'description': 'Battito cardiaco sopra 120 bpm'},
        {'title': 'Paziente {id} - SpO2 Basso', 'description': 'Saturazione ossigeno sotto 92%'},
        {'title': 'Room{room} - Temperatura Alta', 'description': 'Temperatura ambiente sopra 26°C'},
        {'title': 'Room{room} - CO2 Elevato', 'description': 'Livello CO2: {co2} ppm'},
        {'title': 'Asset{asset} - Batteria Bassa', 'description': 'Livello batteria: {battery}%'},
        {'title': 'Asset{asset} - Manutenzione Richiesta', 'description': 'Controllo programmato scaduto'}
    ]
    
    num_alerts = random.randint(2, 5)
    alerts = []
    
    for i in range(num_alerts):
        template = random.choice(alert_templates)
        alert = {
            'title': template['title'].format(
                id=random.randint(1000, 5000),
                room=random.randint(1, 500),
                asset=random.randint(1, 199),
                co2=random.randint(900, 1200),
                battery=random.randint(10, 25)
            ),
            'description': template['description'].format(
                co2=random.randint(900, 1200),
                battery=random.randint(10, 25)
            ),
            'time': f'{random.randint(1, 30)} min fa'
        }
        alerts.append(alert)
    
    return {'alerts': alerts}

def generate_activity():
    """Generate mock recent activity"""
    activities = [
        {'timestamp': '14:32', 'type': 'Patient', 'description': 'Nuovo paziente registrato (P5001)', 'status': 'success'},
        {'timestamp': '14:28', 'type': 'Alert', 'description': 'Allarme risolto - Room 245', 'status': 'success'},
        {'timestamp': '14:15', 'type': 'Asset', 'description': 'Asset 156 spostato in ICU', 'status': 'success'},
        {'timestamp': '14:10', 'type': 'System', 'description': 'Backup dati completato', 'status': 'success'},
        {'timestamp': '14:05', 'type': 'Alert', 'description': 'Nuovo allarme - Paziente P2341', 'status': 'warning'},
    ]
    return {'activities': activities}

# Routes
@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/patients')
def patients():
    """Patients management page"""
    return render_template('patients.html')

@app.route('/rooms')
def rooms():
    """Rooms management page"""
    return render_template('rooms.html')

@app.route('/assets')
def assets():
    """Assets tracking page"""
    return render_template('assets.html')

@app.route('/alerts')
def alerts():
    """Alerts page"""
    return render_template('alerts.html')

@app.route('/analytics')
def analytics():
    """Analytics page"""
    return render_template('analytics.html')

@app.route('/settings')
def settings():
    """Settings page"""
    return render_template('settings.html')

@app.route('/api/patients/latest')
def get_patients():
    """API endpoint for patient data"""
    return jsonify(generate_patient_data())

@app.route('/api/rooms/status')
def get_rooms():
    """API endpoint for room data"""
    return jsonify(generate_room_data())

@app.route('/api/assets/status')
def get_assets():
    """API endpoint for asset data"""
    return jsonify(generate_asset_data())

@app.route('/api/alerts/active')
def get_alerts():
    """API endpoint for active alerts"""
    return jsonify(generate_alerts())

@app.route('/api/activity/recent')
def get_activity():
    """API endpoint for recent activity"""
    return jsonify(generate_activity())

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'IOT Hospital Dashboard'
    })

if __name__ == '__main__':
    print("🏥 IOT Hospital Dashboard Server")
    print("=" * 50)
    print("📊 Dashboard URL: http://localhost:5000")
    print("🔌 API Base URL: http://localhost:5000/api")
    print("=" * 50)
    print("\n✅ Server avviato! Apri il browser su http://localhost:5000\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
