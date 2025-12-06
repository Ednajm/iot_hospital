"""
🏥 IOT Hospital - API RESTful Server
Espone API per consultazione dati IoT

Author: El Houssine (Ednajm)
Corso di Ingegneria Informatica — Progetto IoT 2025
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from database import Database
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Inizializza database
db = Database()

# ============================================
# SYSTEM ENDPOINTS
# ============================================

@app.route('/api/status', methods=['GET'])
def api_status():
    """Status del sistema"""
    stats = db.get_statistics()
    return jsonify({
        "status": "operational",
        "message": "IOT Hospital API Server Running",
        "timestamp": datetime.now().isoformat(),
        "statistics": stats
    })

@app.route('/api/health', methods=['GET'])
def api_health():
    """Health check"""
    return jsonify({
        "status": "healthy",
        "database": "connected",
        "api_version": "1.0.0"
    })

# ============================================
# PATIENT ENDPOINTS
# ============================================

@app.route('/api/patients', methods=['GET'])
def get_patients():
    """
    Ottieni lista pazienti con ultimi dati
    Query params:
    - limit: numero massimo risultati (default 100)
    """
    limit = request.args.get('limit', 100, type=int)
    patients = db.get_all_patients_latest(limit)
    
    return jsonify({
        "count": len(patients),
        "data": patients
    })

@app.route('/api/patients/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    """
    Ottieni dati specifico paziente
    Query params:
    - limit: numero massimo risultati (default 100)
    """
    limit = request.args.get('limit', 100, type=int)
    patient_data = db.get_patient_data(patient_id, limit)
    
    if not patient_data:
        return jsonify({"error": "Paziente non trovato"}), 404
    
    return jsonify({
        "patient_id": patient_id,
        "count": len(patient_data),
        "data": patient_data
    })

@app.route('/api/patients/latest', methods=['GET'])
def get_patients_latest():
    """Ottieni ultimi dati pazienti (per dashboard)"""
    patients = db.get_all_patients_latest(limit=20)
    return jsonify(patients)

# ============================================
# ROOM ENDPOINTS
# ============================================

@app.route('/api/rooms', methods=['GET'])
def get_rooms():
    """
    Ottieni lista stanze con ultimi dati ambientali
    Query params:
    - limit: numero massimo risultati (default 100)
    """
    limit = request.args.get('limit', 100, type=int)
    rooms = db.get_all_rooms_latest(limit)
    
    return jsonify({
        "count": len(rooms),
        "data": rooms
    })

@app.route('/api/rooms/<room_id>', methods=['GET'])
def get_room(room_id):
    """
    Ottieni dati specifica stanza
    Query params:
    - limit: numero massimo risultati (default 100)
    """
    limit = request.args.get('limit', 100, type=int)
    room_data = db.get_room_data(room_id, limit)
    
    if not room_data:
        return jsonify({"error": "Stanza non trovata"}), 404
    
    return jsonify({
        "room_id": room_id,
        "count": len(room_data),
        "data": room_data
    })

@app.route('/api/rooms/status', methods=['GET'])
def get_rooms_status():
    """Ottieni status stanze (per dashboard)"""
    rooms = db.get_all_rooms_latest(limit=20)
    return jsonify(rooms)

# ============================================
# ASSET ENDPOINTS
# ============================================

@app.route('/api/assets', methods=['GET'])
def get_assets():
    """
    Ottieni lista asset con ultimi dati
    Query params:
    - limit: numero massimo risultati (default 100)
    """
    limit = request.args.get('limit', 100, type=int)
    assets = db.get_all_assets_latest(limit)
    
    return jsonify({
        "count": len(assets),
        "data": assets
    })

@app.route('/api/assets/<asset_id>', methods=['GET'])
def get_asset(asset_id):
    """
    Ottieni dati specifico asset
    Query params:
    - limit: numero massimo risultati (default 100)
    """
    limit = request.args.get('limit', 100, type=int)
    asset_data = db.get_asset_data(asset_id, limit)
    
    if not asset_data:
        return jsonify({"error": "Asset non trovato"}), 404
    
    return jsonify({
        "asset_id": asset_id,
        "count": len(asset_data),
        "data": asset_data
    })

@app.route('/api/assets/status', methods=['GET'])
def get_assets_status():
    """Ottieni status asset (per dashboard)"""
    assets = db.get_all_assets_latest(limit=20)
    return jsonify(assets)

# ============================================
# ALERT ENDPOINTS
# ============================================

@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    """
    Ottieni allarmi
    Query params:
    - priority: filtra per priorità (critical, warning, info)
    - acknowledged: mostra solo riconosciuti (0 o 1)
    - limit: numero massimo risultati (default 100)
    """
    priority = request.args.get('priority', None)
    acknowledged = request.args.get('acknowledged', 0, type=int)
    limit = request.args.get('limit', 100, type=int)
    
    alerts = db.get_alerts(
        priority=priority,
        acknowledged=bool(acknowledged),
        limit=limit
    )
    
    return jsonify({
        "count": len(alerts),
        "data": alerts
    })

@app.route('/api/alerts/active', methods=['GET'])
def get_alerts_active():
    """Ottieni allarmi attivi non riconosciuti"""
    alerts = db.get_alerts(acknowledged=False, limit=50)
    return jsonify(alerts)

@app.route('/api/alerts/critical', methods=['GET'])
def get_alerts_critical():
    """Ottieni solo allarmi critici attivi"""
    alerts = db.get_alerts(priority='critical', acknowledged=False, limit=50)
    return jsonify(alerts)

@app.route('/api/alerts/<int:alert_id>/acknowledge', methods=['POST'])
def acknowledge_alert(alert_id):
    """Marca allarme come riconosciuto"""
    try:
        db.acknowledge_alert(alert_id)
        return jsonify({
            "success": True,
            "message": f"Allarme {alert_id} riconosciuto"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ============================================
# STATISTICS ENDPOINTS
# ============================================

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Ottieni statistiche sistema"""
    stats = db.get_statistics()
    return jsonify(stats)

@app.route('/api/dashboard/summary', methods=['GET'])
def get_dashboard_summary():
    """Ottieni riepilogo per dashboard"""
    stats = db.get_statistics()
    
    return jsonify({
        "patients": {
            "total": stats["total_patients"],
            "monitored": stats["total_patients"]
        },
        "rooms": {
            "total": stats["total_rooms"],
            "active": stats["total_rooms"]
        },
        "assets": {
            "total": stats["total_assets"],
            "tracked": stats["total_assets"]
        },
        "alerts": {
            "active": stats["active_alerts"],
            "critical": stats["critical_alerts"]
        }
    })

# ============================================
# ERROR HANDLERS
# ============================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint non trovato"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Errore interno del server"}), 500

# ============================================
# MAIN
# ============================================

if __name__ == '__main__':
    print("=" * 60)
    print("🏥 IOT HOSPITAL - API RESTful Server")
    print("=" * 60)
    print("📚 API Documentation:")
    print("  GET  /api/status              - System status")
    print("  GET  /api/health              - Health check")
    print("  GET  /api/patients            - List patients")
    print("  GET  /api/patients/<id>       - Patient data")
    print("  GET  /api/rooms               - List rooms")
    print("  GET  /api/rooms/<id>          - Room data")
    print("  GET  /api/assets              - List assets")
    print("  GET  /api/assets/<id>         - Asset data")
    print("  GET  /api/alerts              - List alerts")
    print("  GET  /api/alerts/active       - Active alerts")
    print("  GET  /api/alerts/critical     - Critical alerts")
    print("  POST /api/alerts/<id>/ack     - Acknowledge alert")
    print("  GET  /api/statistics          - System statistics")
    print("=" * 60)
    print("🌐 Server running on http://localhost:5000")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5000, debug=True)

