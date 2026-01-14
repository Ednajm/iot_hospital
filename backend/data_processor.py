import json
from typing import Dict, Optional, List
from database import HospitalDatabase

class DataProcessor:
    """
    Processa i dati in arrivo dai sensori MQTT:
    1. Controlla validità
    2. Verifica soglie
    3. Se alert → lo segnala
    4. Chiama database.save(...)
    """
    
    def __init__(self):
        self.db = HospitalDatabase()
        
        # Soglie per pazienti
        self.patient_thresholds = {
            'temperature': {'min': 36.0, 'max': 38.0},
            'spo2': {'min': 90, 'max': 100},
            'heart_rate': {'min': 50, 'max': 120}
        }
        
        # Soglie per stanze
        self.room_thresholds = {
            'temperature': {'min': 18.0, 'max': 28.0},
            'humidity': {'min': 30, 'max': 70},
            'co2': {'min': 0, 'max': 1000}
        }
        
        # Soglie per asset
        self.asset_thresholds = {
            'battery': {'min': 20, 'max': 100}
        }
    
    def validate_patient_data(self, data: Dict) -> bool:
        """Valida i dati del paziente"""
        required_fields = ['patient_id']
        
        # Verifica campi obbligatori
        for field in required_fields:
            if field not in data or data[field] is None:
                return False
        
        # Verifica range valori
        if 'temperature' in data and data['temperature'] is not None:
            if not (30.0 <= data['temperature'] <= 45.0):
                return False
        
        if 'spo2' in data and data['spo2'] is not None:
            if not (0 <= data['spo2'] <= 100):
                return False
        
        if 'heart_rate' in data and data['heart_rate'] is not None:
            if not (0 <= data['heart_rate'] <= 300):
                return False
        
        return True
    
    def validate_room_data(self, data: Dict) -> bool:
        """Valida i dati della stanza"""
        required_fields = ['room_id']
        
        for field in required_fields:
            if field not in data or data[field] is None:
                return False
        
        # Verifica range valori
        if 'temperature' in data and data['temperature'] is not None:
            if not (-10.0 <= data['temperature'] <= 50.0):
                return False
        
        if 'humidity' in data and data['humidity'] is not None:
            if not (0 <= data['humidity'] <= 100):
                return False
        
        if 'co2' in data and data['co2'] is not None:
            if not (0 <= data['co2'] <= 5000):
                return False
        
        return True
    
    def validate_asset_data(self, data: Dict) -> bool:
        """Valida i dati dell'asset"""
        required_fields = ['asset_id']
        
        for field in required_fields:
            if field not in data or data[field] is None:
                return False
        
        if 'battery' in data and data['battery'] is not None:
            if not (0 <= data['battery'] <= 100):
                return False
        
        return True
    
    def check_patient_alerts(self, data: Dict) -> List[Dict]:
        """Verifica le soglie per i pazienti e genera alert"""
        alerts = []
        patient_id = data.get('patient_id')
        
        # Temperatura alta
        if 'temperature' in data and data['temperature'] is not None:
            temp = data['temperature']
            if temp > self.patient_thresholds['temperature']['max']:
                alerts.append({
                    'alert_type': 'HIGH_TEMPERATURE',
                    'entity_id': patient_id,
                    'entity_type': 'patient',
                    'message': f'🌡️ Temperatura alta: {temp}°C',
                    'value': temp,
                    'severity': 'critical' if temp > 39 else 'warning'
                })
            elif temp < self.patient_thresholds['temperature']['min']:
                alerts.append({
                    'alert_type': 'LOW_TEMPERATURE',
                    'entity_id': patient_id,
                    'entity_type': 'patient',
                    'message': f'❄️ Temperatura bassa: {temp}°C',
                    'value': temp,
                    'severity': 'warning'
                })
        
        # SpO2 basso
        if 'spo2' in data and data['spo2'] is not None:
            spo2 = data['spo2']
            if spo2 < self.patient_thresholds['spo2']['min']:
                alerts.append({
                    'alert_type': 'LOW_SPO2',
                    'entity_id': patient_id,
                    'entity_type': 'patient',
                    'message': f'⚠️ SpO₂ basso: {spo2}%',
                    'value': spo2,
                    'severity': 'critical' if spo2 < 85 else 'warning'
                })
        
        # Battito cardiaco anomalo
        if 'heart_rate' in data and data['heart_rate'] is not None:
            hr = data['heart_rate']
            if hr > self.patient_thresholds['heart_rate']['max']:
                alerts.append({
                    'alert_type': 'HIGH_HEART_RATE',
                    'entity_id': patient_id,
                    'entity_type': 'patient',
                    'message': f'💓 Battito alto: {hr} bpm',
                    'value': hr,
                    'severity': 'warning'
                })
            elif hr < self.patient_thresholds['heart_rate']['min']:
                alerts.append({
                    'alert_type': 'LOW_HEART_RATE',
                    'entity_id': patient_id,
                    'entity_type': 'patient',
                    'message': f'💓 Battito basso: {hr} bpm',
                    'value': hr,
                    'severity': 'warning'
                })
        
        return alerts
    
    def check_room_alerts(self, data: Dict) -> List[Dict]:
        """Verifica le soglie per le stanze e genera alert"""
        alerts = []
        room_id = data.get('room_id')
        
        # Temperatura stanza
        if 'temperature' in data and data['temperature'] is not None:
            temp = data['temperature']
            if temp > self.room_thresholds['temperature']['max']:
                alerts.append({
                    'alert_type': 'HIGH_ROOM_TEMP',
                    'entity_id': room_id,
                    'entity_type': 'room',
                    'message': f'🔥 Temperatura stanza alta: {temp}°C',
                    'value': temp,
                    'severity': 'warning'
                })
            elif temp < self.room_thresholds['temperature']['min']:
                alerts.append({
                    'alert_type': 'LOW_ROOM_TEMP',
                    'entity_id': room_id,
                    'entity_type': 'room',
                    'message': f'❄️ Temperatura stanza bassa: {temp}°C',
                    'value': temp,
                    'severity': 'warning'
                })
        
        # Umidità
        if 'humidity' in data and data['humidity'] is not None:
            humidity = data['humidity']
            if humidity > self.room_thresholds['humidity']['max']:
                alerts.append({
                    'alert_type': 'HIGH_HUMIDITY',
                    'entity_id': room_id,
                    'entity_type': 'room',
                    'message': f'💧 Umidità alta: {humidity}%',
                    'value': humidity,
                    'severity': 'warning'
                })
            elif humidity < self.room_thresholds['humidity']['min']:
                alerts.append({
                    'alert_type': 'LOW_HUMIDITY',
                    'entity_id': room_id,
                    'entity_type': 'room',
                    'message': f'🏜️ Umidità bassa: {humidity}%',
                    'value': humidity,
                    'severity': 'warning'
                })
        
        # CO2
        if 'co2' in data and data['co2'] is not None:
            co2 = data['co2']
            if co2 > self.room_thresholds['co2']['max']:
                alerts.append({
                    'alert_type': 'HIGH_CO2',
                    'entity_id': room_id,
                    'entity_type': 'room',
                    'message': f'☁️ CO₂ alto: {co2} ppm',
                    'value': co2,
                    'severity': 'critical' if co2 > 1500 else 'warning'
                })
        
        return alerts
    
    def check_asset_alerts(self, data: Dict) -> List[Dict]:
        """Verifica le soglie per gli asset e genera alert"""
        alerts = []
        asset_id = data.get('asset_id')
        
        # Batteria bassa
        if 'battery' in data and data['battery'] is not None:
            battery = data['battery']
            if battery < self.asset_thresholds['battery']['min']:
                alerts.append({
                    'alert_type': 'LOW_BATTERY',
                    'entity_id': asset_id,
                    'entity_type': 'asset',
                    'message': f'🔋 Batteria bassa: {battery}%',
                    'value': battery,
                    'severity': 'critical' if battery < 10 else 'warning'
                })
        
        # Status manutenzione
        if 'status' in data and data['status'] == 'maintenance':
            alerts.append({
                'alert_type': 'MAINTENANCE',
                'entity_id': asset_id,
                'entity_type': 'asset',
                'message': f'🔧 Asset in manutenzione',
                'value': None,
                'severity': 'info'
            })
        
        return alerts
    
    def process_patient_data(self, data: Dict) -> bool:
        """
        Processa dati paziente:
        1. Valida
        2. Controlla soglie
        3. Genera alert
        4. Salva nel database
        """
        # 1. Valida dati
        if not self.validate_patient_data(data):
            print(f"❌ Dati paziente non validi: {data}")
            return False
        
        # 2. Controlla soglie e genera alert
        alerts = self.check_patient_alerts(data)
        
        # 3. Salva alert
        for alert in alerts:
            self.db.save_alert(alert)
            print(f"🚨 ALERT: {alert['message']}")
        
        # 4. Salva dati nel database
        try:
            self.db.save_patient_data(data)
            return True
        except Exception as e:
            print(f"❌ Errore salvataggio dati paziente: {e}")
            return False
    
    def process_room_data(self, data: Dict) -> bool:
        """
        Processa dati stanza:
        1. Valida
        2. Controlla soglie
        3. Genera alert
        4. Salva nel database
        """
        # 1. Valida dati
        if not self.validate_room_data(data):
            print(f"❌ Dati stanza non validi: {data}")
            return False
        
        # 2. Controlla soglie e genera alert
        alerts = self.check_room_alerts(data)
        
        # 3. Salva alert
        for alert in alerts:
            self.db.save_alert(alert)
            print(f"🚨 ALERT: {alert['message']}")
        
        # 4. Salva dati nel database
        try:
            self.db.save_room_data(data)
            return True
        except Exception as e:
            print(f"❌ Errore salvataggio dati stanza: {e}")
            return False
    
    def process_asset_data(self, data: Dict) -> bool:
        """
        Processa dati asset:
        1. Valida
        2. Controlla soglie
        3. Genera alert
        4. Salva nel database
        """
        # 1. Valida dati
        if not self.validate_asset_data(data):
            print(f"❌ Dati asset non validi: {data}")
            return False
        
        # 2. Controlla soglie e genera alert
        alerts = self.check_asset_alerts(data)
        
        # 3. Salva alert
        for alert in alerts:
            self.db.save_alert(alert)
            print(f"🚨 ALERT: {alert['message']}")
        
        # 4. Salva dati nel database
        try:
            self.db.save_asset_data(data)
            return True
        except Exception as e:
            print(f"❌ Errore salvataggio dati asset: {e}")
            return False


# Test standalone
if __name__ == '__main__':
    processor = DataProcessor()
    
    # Test dati stanza
    test_room_data = {
        'room_id': 'Room1',
        'temperature': 29.5,
        'humidity': 75,
        'co2': 1200
    }
    
    print("🧪 Test processing dati stanza...")
    processor.process_room_data(test_room_data)
    
    # Test dati paziente
    test_patient_data = {
        'patient_id': 'P001',
        'temperature': 39.2,
        'spo2': 87,
        'heart_rate': 135,
        'room_id': 'Room1'
    }
    
    print("\n🧪 Test processing dati paziente...")
    processor.process_patient_data(test_patient_data)
    
    # Mostra statistiche
    print("\n📊 Statistiche database:")
    stats = processor.db.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Mostra alert attivi
    print("\n🚨 Alert attivi:")
    alerts = processor.db.get_active_alerts(limit=10)
    for alert in alerts:
        print(f"  [{alert['severity']}] {alert['message']}")
    



