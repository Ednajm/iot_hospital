"""
🏥 IOT Hospital - Database Manager
Gestisce storage e retrieval dei dati IoT in SQLite

Author: El Houssine (Ednajm)
Corso di Ingegneria Informatica — Progetto IoT 2025
"""

import sqlite3
import json
from datetime import datetime
import os

class Database:
    """
    Gestisce database SQLite per memorizzare dati sensori e allarmi
    """
    
    def __init__(self, db_path="data/iot_hospital.db"):
        self.db_path = db_path
        self._ensure_data_directory()
        self.init_database()
        print(f"💾 Database inizializzato: {db_path}")
    
    def _ensure_data_directory(self):
        """Crea directory data se non esiste"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
    
    def get_connection(self):
        """Ottieni connessione al database"""
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Inizializza tabelle database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tabella pazienti
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                heart_rate INTEGER,
                temperature REAL,
                spo2 INTEGER,
                timestamp TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabella stanze
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rooms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                room_id TEXT NOT NULL,
                temperature REAL,
                humidity INTEGER,
                co2 INTEGER,
                timestamp TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabella asset
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS assets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                asset_id TEXT NOT NULL,
                location TEXT,
                status TEXT,
                battery INTEGER,
                timestamp TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabella allarmi
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                alert_type TEXT NOT NULL,
                priority TEXT NOT NULL,
                entity_id TEXT NOT NULL,
                parameter TEXT,
                value REAL,
                threshold REAL,
                message TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                acknowledged BOOLEAN DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Indici per performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_patients_id ON patients(patient_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_rooms_id ON rooms(room_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_assets_id ON assets(asset_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_alerts_type ON alerts(alert_type)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_alerts_priority ON alerts(priority)')
        
        conn.commit()
        conn.close()
    
    # ============================================
    # PATIENT DATA
    # ============================================
    
    def save_patient_data(self, patient_id, heart_rate, temperature, spo2, timestamp):
        """Salva dati paziente"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO patients (patient_id, heart_rate, temperature, spo2, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (patient_id, heart_rate, temperature, spo2, timestamp))
        
        conn.commit()
        conn.close()
    
    def get_patient_data(self, patient_id, limit=100):
        """Recupera dati paziente"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM patients 
            WHERE patient_id = ? 
            ORDER BY created_at DESC 
            LIMIT ?
        ''', (patient_id, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_dict(row, cursor) for row in rows]
    
    def get_all_patients_latest(self, limit=100):
        """Recupera ultimi dati di tutti i pazienti"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM patients 
            ORDER BY created_at DESC 
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_dict(row, cursor) for row in rows]
    
    # ============================================
    # ROOM DATA
    # ============================================
    
    def save_room_data(self, room_id, temperature, humidity, co2, timestamp):
        """Salva dati stanza"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO rooms (room_id, temperature, humidity, co2, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (room_id, temperature, humidity, co2, timestamp))
        
        conn.commit()
        conn.close()
    
    def get_room_data(self, room_id, limit=100):
        """Recupera dati stanza"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM rooms 
            WHERE room_id = ? 
            ORDER BY created_at DESC 
            LIMIT ?
        ''', (room_id, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_dict(row, cursor) for row in rows]
    
    def get_all_rooms_latest(self, limit=100):
        """Recupera ultimi dati di tutte le stanze"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM rooms 
            ORDER BY created_at DESC 
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_dict(row, cursor) for row in rows]
    
    # ============================================
    # ASSET DATA
    # ============================================
    
    def save_asset_data(self, asset_id, location, status, battery, timestamp):
        """Salva dati asset"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO assets (asset_id, location, status, battery, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (asset_id, location, status, battery, timestamp))
        
        conn.commit()
        conn.close()
    
    def get_asset_data(self, asset_id, limit=100):
        """Recupera dati asset"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM assets 
            WHERE asset_id = ? 
            ORDER BY created_at DESC 
            LIMIT ?
        ''', (asset_id, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_dict(row, cursor) for row in rows]
    
    def get_all_assets_latest(self, limit=100):
        """Recupera ultimi dati di tutti gli asset"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM assets 
            ORDER BY created_at DESC 
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_dict(row, cursor) for row in rows]
    
    # ============================================
    # ALERTS
    # ============================================
    
    def save_alert(self, alert_data):
        """Salva allarme"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        entity_id = alert_data.get('patient_id') or alert_data.get('room_id') or alert_data.get('asset_id', 'unknown')
        
        cursor.execute('''
            INSERT INTO alerts (alert_type, priority, entity_id, parameter, value, threshold, message, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            alert_data.get('type'),
            alert_data.get('priority'),
            str(entity_id),
            alert_data.get('parameter'),
            alert_data.get('value'),
            alert_data.get('threshold'),
            alert_data.get('message'),
            alert_data.get('timestamp')
        ))
        
        conn.commit()
        conn.close()
    
    def get_alerts(self, priority=None, acknowledged=False, limit=100):
        """Recupera allarmi"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = 'SELECT * FROM alerts WHERE acknowledged = ?'
        params = [1 if acknowledged else 0]
        
        if priority:
            query += ' AND priority = ?'
            params.append(priority)
        
        query += ' ORDER BY created_at DESC LIMIT ?'
        params.append(limit)
        
        cursor.execute(query, params)
        
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_dict(row, cursor) for row in rows]
    
    def acknowledge_alert(self, alert_id):
        """Marca allarme come riconosciuto"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('UPDATE alerts SET acknowledged = 1 WHERE id = ?', (alert_id,))
        
        conn.commit()
        conn.close()
    
    # ============================================
    # STATISTICS
    # ============================================
    
    def get_statistics(self):
        """Ottieni statistiche generali"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Count pazienti
        cursor.execute('SELECT COUNT(DISTINCT patient_id) FROM patients')
        total_patients = cursor.fetchone()[0]
        
        # Count stanze
        cursor.execute('SELECT COUNT(DISTINCT room_id) FROM rooms')
        total_rooms = cursor.fetchone()[0]
        
        # Count asset
        cursor.execute('SELECT COUNT(DISTINCT asset_id) FROM assets')
        total_assets = cursor.fetchone()[0]
        
        # Count allarmi attivi
        cursor.execute('SELECT COUNT(*) FROM alerts WHERE acknowledged = 0')
        active_alerts = cursor.fetchone()[0]
        
        # Count allarmi critici
        cursor.execute('SELECT COUNT(*) FROM alerts WHERE acknowledged = 0 AND priority = ?', ('critical',))
        critical_alerts = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "total_patients": total_patients,
            "total_rooms": total_rooms,
            "total_assets": total_assets,
            "active_alerts": active_alerts,
            "critical_alerts": critical_alerts
        }
    
    def _row_to_dict(self, row, cursor):
        """Converti row SQL in dict"""
        if not row:
            return None
        return dict(zip([column[0] for column in cursor.description], row))
    
    def clear_old_data(self, days=30):
        """Elimina dati vecchi (pulizia database)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(f"DELETE FROM patients WHERE created_at < datetime('now', '-{days} days')")
        cursor.execute(f"DELETE FROM rooms WHERE created_at < datetime('now', '-{days} days')")
        cursor.execute(f"DELETE FROM assets WHERE created_at < datetime('now', '-{days} days')")
        cursor.execute(f"DELETE FROM alerts WHERE acknowledged = 1 AND created_at < datetime('now', '-{days} days')")
        
        conn.commit()
        conn.close()
        
        print(f"🗑️  Dati più vecchi di {days} giorni eliminati")

if __name__ == "__main__":
    # Test database
    db = Database()
    
    print("\n📊 Statistiche database:")
    stats = db.get_statistics()
    for key, value in stats.items():
        print(f"  - {key}: {value}")
