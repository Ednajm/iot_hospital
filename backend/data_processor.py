import pandas as pd
import json
import os
PATIENT_FILE = 'data/patients_data.csv'
ROOM_FILE = 'data/room_data.csv'
ASSET_FILE = 'data/asset_data.csv'
ALERT_FILE = 'data/alerts.json'
if not (os.path.exists(PATIENT_FILE) and os.path.exists(ROOM_FILE) and os.path.exists(ASSET_FILE)):
    print(" Errore: uno o più file CSV non trovati nella cartella /data.")
    exit()
patient_df = pd.read_csv(PATIENT_FILE)
room_df = pd.read_csv(ROOM_FILE)
asset_df = pd.read_csv(ASSET_FILE)
alerts = []
for index, row in patient_df.iterrows():
    patient_id = row.get("patient_id")
    temperature = row.get("temperature")
    spo2 = row.get("spo2")
    heart_rate = row.get("heart_rate")
    room_id = row.get("room_id")
    if temperature and temperature > 38:
        alerts.append({
            "type": "Patient",
            "id": patient_id,
            "room": room_id,
            "alert": " High Temperature",
            "value": temperature
        })
    if spo2 and spo2 < 90:
        alerts.append({
            "type": "Patient",
            "id": patient_id,
            "room": room_id,
            "alert": " Low SpO₂",
            "value": spo2
        })
    if heart_rate and (heart_rate < 50 or heart_rate > 120):
        alerts.append({
            "type": "Patient",
            "id": patient_id,
            "room": room_id,
            "alert": " Abnormal Heart Rate",
            "value": heart_rate
        })
for index, row in room_df.iterrows():
    room_id = row.get("room_id")
    temperature = row.get("temperature")
    humidity = row.get("humidity")
    co2 = row.get("co2")

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
    



