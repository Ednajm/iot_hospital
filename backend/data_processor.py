from typing import Dict, List
from database import HospitalDatabase

class DataProcessor:
    def __init__(self):
        self.db = HospitalDatabase()
        self.thresholds = {
            'patient': {'temperature': (36.0, 38.0), 'spo2': (90, 100), 'heart_rate': (50, 120)},
            'room': {'temperature': (18.0, 28.0), 'humidity': (30, 70), 'co2': (0, 1000)},
            'asset': {'battery': (20, 100)}
        }
        self.validation_ranges = {
            'patient': {'temperature': (30.0, 45.0), 'spo2': (0, 100), 'heart_rate': (0, 300)},
            'room': {'temperature': (-10.0, 50.0), 'humidity': (0, 100), 'co2': (0, 5000)},
            'asset': {'battery': (0, 100)}
        }
    
    def _validate(self, data: Dict, entity_type: str) -> bool:
        id_key = f'{entity_type}_id'
        if id_key not in data or data[id_key] is None: return False
        for key, (min_val, max_val) in self.validation_ranges[entity_type].items():
            if key in data and data[key] is not None:
                if not (min_val <= data[key] <= max_val): return False
        return True
    
    def _check_alerts(self, data: Dict, entity_type: str) -> List[Dict]:
        alerts = []
        entity_id = data.get(f'{entity_type}_id')
        alert_configs = {
            'patient': [
                ('temperature', 'TEMPERATURE', '°C', lambda v, t: 'critical' if v > 39 or v < 35 else 'warning'),
                ('spo2', 'SPO2', '%', lambda v, t: 'critical' if v < 85 else 'warning'),
                ('heart_rate', 'HEART_RATE', ' bpm', lambda v, t: 'warning')
            ],
            'room': [
                ('temperature', 'ROOM_TEMP', '°C', lambda v, t: 'warning'),
                ('humidity', 'HUMIDITY', '%', lambda v, t: 'warning'),
                ('co2', 'CO2', ' ppm', lambda v, t: 'critical' if v > 1500 else 'warning')
            ]
        }
        
        if entity_type in alert_configs:
            for metric, alert_name, unit, severity_fn in alert_configs[entity_type]:
                if metric in data and data[metric] is not None:
                    val = data[metric]
                    min_t, max_t = self.thresholds[entity_type][metric]
                    if val > max_t:
                        alerts.append({'alert_type': f'HIGH_{alert_name}', 'entity_id': entity_id, 'entity_type': entity_type, 
                                     'message': f'{metric.capitalize()} alto: {val}{unit}', 'value': val, 'severity': severity_fn(val, max_t)})
                    elif val < min_t:
                        alerts.append({'alert_type': f'LOW_{alert_name}', 'entity_id': entity_id, 'entity_type': entity_type,
                                     'message': f'{metric.capitalize()} basso: {val}{unit}', 'value': val, 'severity': severity_fn(val, min_t)})
        
        if entity_type == 'asset':
            if 'battery' in data and data['battery'] is not None and data['battery'] < self.thresholds['asset']['battery'][0]:
                alerts.append({'alert_type': 'LOW_BATTERY', 'entity_id': entity_id, 'entity_type': 'asset',
                             'message': f'Batteria bassa: {data["battery"]}%', 'value': data['battery'], 
                             'severity': 'critical' if data['battery'] < 10 else 'warning'})
            if data.get('status') == 'maintenance':
                alerts.append({'alert_type': 'MAINTENANCE', 'entity_id': entity_id, 'entity_type': 'asset',
                             'message': 'Asset in manutenzione', 'value': None, 'severity': 'info'})
        return alerts
    
    def _process(self, data: Dict, entity_type: str) -> bool:
        if not self._validate(data, entity_type): return False
        for alert in self._check_alerts(data, entity_type): self.db.save_alert(alert)
        try:
            getattr(self.db, f'save_{entity_type}_data')(data)
            return True
        except: return False
    
    def validate_patient_data(self, data: Dict) -> bool: return self._validate(data, 'patient')
    def validate_room_data(self, data: Dict) -> bool: return self._validate(data, 'room')
    def validate_asset_data(self, data: Dict) -> bool: return self._validate(data, 'asset')
    def check_patient_alerts(self, data: Dict) -> List[Dict]: return self._check_alerts(data, 'patient')
    def check_room_alerts(self, data: Dict) -> List[Dict]: return self._check_alerts(data, 'room')
    def check_asset_alerts(self, data: Dict) -> List[Dict]: return self._check_alerts(data, 'asset')
    def process_patient_data(self, data: Dict) -> bool: return self._process(data, 'patient')
    def process_room_data(self, data: Dict) -> bool: return self._process(data, 'room')
    def process_asset_data(self, data: Dict) -> bool: return self._process(data, 'asset')
