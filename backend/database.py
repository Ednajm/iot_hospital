import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Optional

class HospitalDatabase:
    def __init__(self, db_path='data/hospital.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Inizializza le tabelle del database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabella per dati pazienti
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patient_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id TEXT NOT NULL,
                temperature REAL,
                spo2 INTEGER,
                heart_rate INTEGER,
                room_id TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabella per dati stanze
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS room_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                room_id TEXT NOT NULL,
                temperature REAL,
                humidity INTEGER,
                co2 INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabella per asset tracking
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS asset_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                asset_id TEXT NOT NULL,
                location TEXT,
                battery INTEGER,
                status TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabella per alert
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                alert_type TEXT NOT NULL,
                entity_id TEXT NOT NULL,
                entity_type TEXT NOT NULL,
                message TEXT NOT NULL,
                value REAL,
                severity TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                acknowledged INTEGER DEFAULT 0
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Database inizializzato")
    
    def save_patient_data(self, data: Dict):
        """Salva dati paziente nel database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO patient_data (patient_id, temperature, spo2, heart_rate, room_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            data.get('patient_id'),
            data.get('temperature'),
            data.get('spo2'),
            data.get('heart_rate'),
            data.get('room_id')
        ))
        
        conn.commit()
        conn.close()
    
    def save_room_data(self, data: Dict):
        """Salva dati stanza nel database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO room_data (room_id, temperature, humidity, co2)
            VALUES (?, ?, ?, ?)
        ''', (
            data.get('room_id'),
            data.get('temperature'),
            data.get('humidity'),
            data.get('co2')
        ))
        
        conn.commit()
        conn.close()
    
    def save_asset_data(self, data: Dict):
        """Salva dati asset nel database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO asset_data (asset_id, location, battery, status)
            VALUES (?, ?, ?, ?)
        ''', (
            data.get('asset_id'),
            data.get('location'),
            data.get('battery'),
            data.get('status')
        ))
        
        conn.commit()
        conn.close()
    
    def save_alert(self, alert: Dict):
        """Salva alert nel database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO alerts (alert_type, entity_id, entity_type, message, value, severity)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            alert.get('alert_type'),
            alert.get('entity_id'),
            alert.get('entity_type'),
            alert.get('message'),
            alert.get('value'),
            alert.get('severity', 'warning')
        ))
        
        conn.commit()
        conn.close()
    
    # Funzioni di lettura
    
    def get_latest_patient_data(self, patient_id: str) -> Optional[Dict]:
        """Ottieni ultimi dati di un paziente"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM patient_data 
            WHERE patient_id = ? 
            ORDER BY timestamp DESC 
            LIMIT 1
        ''', (patient_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        return dict(row) if row else None
    
    def get_latest_room_data(self, room_id: str) -> Optional[Dict]:
        """Ottieni ultimi dati di una stanza"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM room_data 
            WHERE room_id = ? 
            ORDER BY timestamp DESC 
            LIMIT 1
        ''', (room_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        return dict(row) if row else None
    
    def get_all_rooms_status(self) -> List[Dict]:
        """Ottieni stato di tutte le stanze"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT room_id, temperature, humidity, co2, MAX(timestamp) as timestamp
            FROM room_data 
            GROUP BY room_id
            ORDER BY room_id
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_active_alerts(self, limit: int = 50) -> List[Dict]:
        """Ottieni alert attivi (non riconosciuti)"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM alerts 
            WHERE acknowledged = 0 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_all_alerts(self, limit: int = 100) -> List[Dict]:
        """Ottieni tutti gli alert"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM alerts 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def acknowledge_alert(self, alert_id: int):
        """Riconosci un alert"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE alerts 
            SET acknowledged = 1 
            WHERE id = ?
        ''', (alert_id,))
        
        conn.commit()
        conn.close()
    
    def get_patient_history(self, patient_id: str, limit: int = 100) -> List[Dict]:
        """Ottieni storico dati paziente"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM patient_data 
            WHERE patient_id = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (patient_id, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_room_history(self, room_id: str, limit: int = 100) -> List[Dict]:
        """Ottieni storico dati stanza"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM room_data 
            WHERE room_id = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (room_id, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_statistics(self) -> Dict:
        """Ottieni statistiche generali"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        stats = {}
        
        # Conta record
        cursor.execute('SELECT COUNT(*) FROM patient_data')
        stats['total_patient_records'] = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM room_data')
        stats['total_room_records'] = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM asset_data')
        stats['total_asset_records'] = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM alerts WHERE acknowledged = 0')
        stats['active_alerts'] = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM alerts')
        stats['total_alerts'] = cursor.fetchone()[0]
        
        conn.close()
        
        return stats
