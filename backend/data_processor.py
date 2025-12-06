"""
🏥 IOT Hospital - Data Processor
Elabora dati dai sensori e genera allarmi in base a soglie critiche

Author: El Houssine (Ednajm)
Corso di Ingegneria Informatica — Progetto IoT 2025
"""

from datetime import datetime
import json

class DataProcessor:
    """
    Elabora i dati dei sensori e genera allarmi basati su soglie critiche
    """
    
    # Soglie parametri pazienti (come da README)
    PATIENT_THRESHOLDS = {
        "heart_rate_min": 60,
        "heart_rate_max": 120,
        "temperature_normal": 38.0,
        "temperature_critical": 38.5,
        "spo2_critical": 92,
        "spo2_min": 90
    }
    
    # Soglie parametri ambientali (come da README)
    ROOM_THRESHOLDS = {
        "temperature_min": 20,
        "temperature_max": 26,
        "humidity_min": 40,
        "humidity_max": 65,
        "co2_normal": 800,
        "co2_critical": 1000
    }
    
    # Soglie asset (come da README)
    ASSET_THRESHOLDS = {
        "battery_low": 25,
        "battery_critical": 20
    }
    
    def __init__(self):
        print("🔧 DataProcessor inizializzato con soglie critiche")
    
    def check_patient_alerts(self, patient_id, heart_rate, temperature, spo2):
        """
        Verifica parametri vitali paziente e genera allarmi
        
        Parametri monitorati:
        - Battito cardiaco: 60-120 bpm
        - Temperatura: < 38.5°C (allarme se > 38°C)
        - SpO₂: 90-100% (allarme se < 92%)
        """
        alerts = []
        timestamp = datetime.now().isoformat()
        
        # Verifica battito cardiaco
        if heart_rate < self.PATIENT_THRESHOLDS["heart_rate_min"]:
            alerts.append({
                "type": "patient",
                "priority": "critical",
                "patient_id": patient_id,
                "parameter": "heart_rate",
                "value": heart_rate,
                "threshold": self.PATIENT_THRESHOLDS["heart_rate_min"],
                "message": f"Battito cardiaco troppo basso: {heart_rate} bpm (min {self.PATIENT_THRESHOLDS['heart_rate_min']})",
                "timestamp": timestamp
            })
        elif heart_rate > self.PATIENT_THRESHOLDS["heart_rate_max"]:
            alerts.append({
                "type": "patient",
                "priority": "critical",
                "patient_id": patient_id,
                "parameter": "heart_rate",
                "value": heart_rate,
                "threshold": self.PATIENT_THRESHOLDS["heart_rate_max"],
                "message": f"Battito cardiaco troppo alto: {heart_rate} bpm (max {self.PATIENT_THRESHOLDS['heart_rate_max']})",
                "timestamp": timestamp
            })
        
        # Verifica temperatura
        if temperature >= self.PATIENT_THRESHOLDS["temperature_critical"]:
            alerts.append({
                "type": "patient",
                "priority": "critical",
                "patient_id": patient_id,
                "parameter": "temperature",
                "value": temperature,
                "threshold": self.PATIENT_THRESHOLDS["temperature_critical"],
                "message": f"Temperatura critica: {temperature}°C (max {self.PATIENT_THRESHOLDS['temperature_critical']}°C)",
                "timestamp": timestamp
            })
        elif temperature > self.PATIENT_THRESHOLDS["temperature_normal"]:
            alerts.append({
                "type": "patient",
                "priority": "warning",
                "patient_id": patient_id,
                "parameter": "temperature",
                "value": temperature,
                "threshold": self.PATIENT_THRESHOLDS["temperature_normal"],
                "message": f"Temperatura elevata: {temperature}°C (normale < {self.PATIENT_THRESHOLDS['temperature_normal']}°C)",
                "timestamp": timestamp
            })
        
        # Verifica SpO2
        if spo2 < self.PATIENT_THRESHOLDS["spo2_critical"]:
            alerts.append({
                "type": "patient",
                "priority": "critical",
                "patient_id": patient_id,
                "parameter": "spo2",
                "value": spo2,
                "threshold": self.PATIENT_THRESHOLDS["spo2_critical"],
                "message": f"Saturazione ossigeno critica: {spo2}% (min {self.PATIENT_THRESHOLDS['spo2_critical']}%)",
                "timestamp": timestamp
            })
        elif spo2 < self.PATIENT_THRESHOLDS["spo2_min"]:
            alerts.append({
                "type": "patient",
                "priority": "warning",
                "patient_id": patient_id,
                "parameter": "spo2",
                "value": spo2,
                "threshold": self.PATIENT_THRESHOLDS["spo2_min"],
                "message": f"Saturazione ossigeno bassa: {spo2}% (min {self.PATIENT_THRESHOLDS['spo2_min']}%)",
                "timestamp": timestamp
            })
        
        return alerts
    
    def check_room_alerts(self, room_id, temperature, humidity, co2):
        """
        Verifica parametri ambientali stanza e genera allarmi
        
        Parametri monitorati:
        - Temperatura: 20-26°C
        - Umidità: 40-65%
        - CO2: 400-800 ppm (allarme se > 1000 ppm)
        """
        alerts = []
        timestamp = datetime.now().isoformat()
        
        # Verifica temperatura
        if temperature < self.ROOM_THRESHOLDS["temperature_min"]:
            alerts.append({
                "type": "room",
                "priority": "warning",
                "room_id": room_id,
                "parameter": "temperature",
                "value": temperature,
                "threshold": self.ROOM_THRESHOLDS["temperature_min"],
                "message": f"Temperatura stanza troppo bassa: {temperature}°C (min {self.ROOM_THRESHOLDS['temperature_min']}°C)",
                "timestamp": timestamp
            })
        elif temperature > self.ROOM_THRESHOLDS["temperature_max"]:
            alerts.append({
                "type": "room",
                "priority": "warning",
                "room_id": room_id,
                "parameter": "temperature",
                "value": temperature,
                "threshold": self.ROOM_THRESHOLDS["temperature_max"],
                "message": f"Temperatura stanza troppo alta: {temperature}°C (max {self.ROOM_THRESHOLDS['temperature_max']}°C)",
                "timestamp": timestamp
            })
        
        # Verifica umidità
        if humidity < self.ROOM_THRESHOLDS["humidity_min"]:
            alerts.append({
                "type": "room",
                "priority": "info",
                "room_id": room_id,
                "parameter": "humidity",
                "value": humidity,
                "threshold": self.ROOM_THRESHOLDS["humidity_min"],
                "message": f"Umidità troppo bassa: {humidity}% (min {self.ROOM_THRESHOLDS['humidity_min']}%)",
                "timestamp": timestamp
            })
        elif humidity > self.ROOM_THRESHOLDS["humidity_max"]:
            alerts.append({
                "type": "room",
                "priority": "info",
                "room_id": room_id,
                "parameter": "humidity",
                "value": humidity,
                "threshold": self.ROOM_THRESHOLDS["humidity_max"],
                "message": f"Umidità troppo alta: {humidity}% (max {self.ROOM_THRESHOLDS['humidity_max']}%)",
                "timestamp": timestamp
            })
        
        # Verifica CO2
        if co2 > self.ROOM_THRESHOLDS["co2_critical"]:
            alerts.append({
                "type": "room",
                "priority": "critical",
                "room_id": room_id,
                "parameter": "co2",
                "value": co2,
                "threshold": self.ROOM_THRESHOLDS["co2_critical"],
                "message": f"Livello CO2 critico: {co2} ppm (max {self.ROOM_THRESHOLDS['co2_critical']} ppm)",
                "timestamp": timestamp
            })
        elif co2 > self.ROOM_THRESHOLDS["co2_normal"]:
            alerts.append({
                "type": "room",
                "priority": "warning",
                "room_id": room_id,
                "parameter": "co2",
                "value": co2,
                "threshold": self.ROOM_THRESHOLDS["co2_normal"],
                "message": f"Livello CO2 elevato: {co2} ppm (normale < {self.ROOM_THRESHOLDS['co2_normal']} ppm)",
                "timestamp": timestamp
            })
        
        return alerts
    
    def check_asset_alerts(self, asset_id, battery, status):
        """
        Verifica stato asset e genera allarmi
        
        Parametri monitorati:
        - Batteria: > 20% (allarme se < 25%)
        - Stato: Active, Standby, Maintenance
        """
        alerts = []
        timestamp = datetime.now().isoformat()
        
        # Verifica batteria
        if battery < self.ASSET_THRESHOLDS["battery_critical"]:
            alerts.append({
                "type": "asset",
                "priority": "critical",
                "asset_id": asset_id,
                "parameter": "battery",
                "value": battery,
                "threshold": self.ASSET_THRESHOLDS["battery_critical"],
                "message": f"Batteria critica: {battery}% (min {self.ASSET_THRESHOLDS['battery_critical']}%)",
                "timestamp": timestamp
            })
        elif battery < self.ASSET_THRESHOLDS["battery_low"]:
            alerts.append({
                "type": "asset",
                "priority": "warning",
                "asset_id": asset_id,
                "parameter": "battery",
                "value": battery,
                "threshold": self.ASSET_THRESHOLDS["battery_low"],
                "message": f"Batteria bassa: {battery}% (min {self.ASSET_THRESHOLDS['battery_low']}%)",
                "timestamp": timestamp
            })
        
        # Verifica stato manutenzione
        if status.lower() == "maintenance":
            alerts.append({
                "type": "asset",
                "priority": "info",
                "asset_id": asset_id,
                "parameter": "status",
                "value": status,
                "message": f"Asset in manutenzione: {asset_id}",
                "timestamp": timestamp
            })
        
        return alerts
    
    def analyze_trends(self, data_series):
        """
        Analizza trend dei dati per predire anomalie
        (Da implementare in futuro per ML/AI)
        """
        pass
    
    def get_statistics(self, data_list):
        """
        Calcola statistiche sui dati raccolti
        """
        if not data_list:
            return {}
        
        return {
            "count": len(data_list),
            "min": min(data_list),
            "max": max(data_list),
            "avg": sum(data_list) / len(data_list)
        }

if __name__ == "__main__":
    # Test del processor
    processor = DataProcessor()
    
    print("\n🧪 Test soglie pazienti:")
    alerts = processor.check_patient_alerts(1234, 45, 39.0, 88)
    for alert in alerts:
        print(f"  - {alert['priority'].upper()}: {alert['message']}")
    
    print("\n🧪 Test soglie ambientali:")
    alerts = processor.check_room_alerts("Room101", 28, 70, 1200)
    for alert in alerts:
        print(f"  - {alert['priority'].upper()}: {alert['message']}")
    
    print("\n🧪 Test soglie asset:")
    alerts = processor.check_asset_alerts("Asset001", 15, "maintenance")
    for alert in alerts:
        print(f"  - {alert['priority'].upper()}: {alert['message']}")

    if temperature and (temperature < 18 or temperature > 30):
        alerts.append({
            "type": "Room",
            "id": room_id,
            "alert": " Room Temperature Out of Range",
            "value": temperature
        })
    if humidity and (humidity < 30 or humidity > 70):
        alerts.append({
            "type": "Room",
            "id": room_id,
            "alert": " Humidity Out of Range",
            "value": humidity
        })
    if co2 and co2 > 1000:
        alerts.append({
            "type": "Room",
            "id": room_id,
            "alert": "High CO₂ Level",
            "value": co2
        })

for index, row in asset_df.iterrows():
    asset_id = row.get("asset_id")
    battery = row.get("battery")
    status = row.get("status")

    if battery and battery < 25:
        alerts.append({
            "type": "Asset",
            "id": asset_id,
            "alert": " Low Battery Level",
            "value": battery
        })
    if status == "maintenance":
        alerts.append({
            "type": "Asset",
            "id": asset_id,
            "alert": " Asset Under Maintenance",
            "value": None
        })
if alerts:
    with open(ALERT_FILE, 'w', encoding='utf-8') as f:
        json.dump(alerts, f, indent=4, ensure_ascii=False)
    print(f" {len(alerts)} alert salvati in {ALERT_FILE}")
else:
    print("Nessun alert rilevato – Tutto normale")
print("\n Riepilogo alert:")
for alert in alerts[:10]: 
    print(f"[{alert['type']}] {alert['id']} → {alert['alert']} ({alert['value'] if 'value' in alert else ''})")
    



