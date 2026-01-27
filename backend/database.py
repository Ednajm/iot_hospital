import sqlite3

class HospitalDatabase:
    def get_all_rooms_status(self):
        return self._q('SELECT * FROM room_data ORDER BY ts DESC', (), 2)

    def get_statistics(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute('SELECT COUNT(*) FROM patient_data')
        total_patient_records = cur.fetchone()[0]
        cur.execute('SELECT COUNT(*) FROM asset_data')
        total_asset_records = cur.fetchone()[0]
        conn.close()
        return {
            'total_patient_records': total_patient_records,
            'total_asset_records': total_asset_records
        }

    def __init__(self, db_path='data/hospital.db'):
        self.db_path = db_path
        self._init_db()

    def _q(self, sql, params=(), fetch=None):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row if fetch else None
        cur = conn.execute(sql, params)
        res = dict(cur.fetchone()) if fetch == 1 and cur.fetchone() else [dict(r) for r in cur.fetchall()] if fetch else None
        conn.commit(); conn.close()
        return res

    def _init_db(self):
        sql = '''CREATE TABLE IF NOT EXISTS patient_data(id INTEGER PRIMARY KEY,patient_id TEXT,temperature REAL,spo2 INT,heart_rate INT,room_id TEXT,ts DATETIME DEFAULT CURRENT_TIMESTAMP);
        CREATE TABLE IF NOT EXISTS room_data(id INTEGER PRIMARY KEY,room_id TEXT,temperature REAL,humidity INT,co2 INT,ts DATETIME DEFAULT CURRENT_TIMESTAMP);
        CREATE TABLE IF NOT EXISTS asset_data(id INTEGER PRIMARY KEY,asset_id TEXT,location TEXT,status TEXT,battery INT,ts DATETIME DEFAULT CURRENT_TIMESTAMP);
        CREATE TABLE IF NOT EXISTS alerts(id INTEGER PRIMARY KEY,type TEXT,entity_id TEXT,msg TEXT,value REAL,severity TEXT,ts DATETIME DEFAULT CURRENT_TIMESTAMP,ack INT DEFAULT 0)'''
        conn = sqlite3.connect(self.db_path)
        conn.executescript(sql); conn.close()

    def save_patient_data(self, d):
        self._q('INSERT INTO patient_data(patient_id,temperature,spo2,heart_rate,room_id)VALUES(?,?,?,?,?)', tuple(d.get(k) for k in ['patient_id','temperature','spo2','heart_rate','room_id']))

    def save_room_data(self, d):
        self._q('INSERT INTO room_data(room_id,temperature,humidity,co2)VALUES(?,?,?,?)', tuple(d.get(k) for k in ['room_id','temperature','humidity','co2']))

    def save_asset_data(self, d):
        self._q('INSERT INTO asset_data(asset_id,location,status,battery)VALUES(?,?,?,?)', tuple(d.get(k) for k in ['asset_id','location','status','battery']))

    def save_alert(self, d):
        self._q('INSERT INTO alerts(type,entity_id,msg,value,severity)VALUES(?,?,?,?,?)', (d.get('alert_type'),d.get('entity_id'),d.get('message'),d.get('value'),d.get('severity','warning')))

    def get_patient(self, pid):
        return self._q('SELECT * FROM patient_data WHERE patient_id=? ORDER BY ts DESC LIMIT 1', (pid,), 1)

    def get_room(self, rid):
        return self._q('SELECT * FROM room_data WHERE room_id=? ORDER BY ts DESC LIMIT 1', (rid,), 1)

    def get_alerts(self, active=True, limit=50):
        return self._q(f'SELECT * FROM alerts {"WHERE ack=0" if active else ""} ORDER BY ts DESC LIMIT ?', (limit,), 2)

    def ack_alert(self, id):
        self._q('UPDATE alerts SET ack=1 WHERE id=?', (id,))
    def get_history(self, table, id_col, id_val, limit=100): return self._q(f'SELECT * FROM {table} WHERE {id_col}=? ORDER BY ts DESC LIMIT ?', (id_val,limit), 2)
