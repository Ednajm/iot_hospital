import paho.mqtt.client as mqtt
import logging
import time
import json
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_processor import DataProcessor
from database import HospitalDatabase

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db = HospitalDatabase(db_path=os.path.join(project_root, 'data', 'hospital.db'))
processor = DataProcessor()

# Configurazione MQTT
BROKER = "localhost"
PORT = 1883
TOPICS = [
    "hospital/patient/+",
    "hospital/room/+",
    "hospital/asset/+",
]
QOS = 1
RECONNECT_MAX_RETRY = 5
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info("Connected to MQTT broker")
        for t in TOPICS:
            client.subscribe(t, QOS)
            logging.info("Subscribed to topic: %s", t)
    else:
        logging.error("Failed to connect, return code %d", rc)


def on_disconnect(client, userdata, rc):
    if rc != 0:
        logging.warning("Unexpected disconnection. Attempting to reconnect...")
        for attempt in range(RECONNECT_MAX_RETRY):
            try:
                client.reconnect()
                logging.info("Reconnected to MQTT broker")
                return
            except Exception as e:
                logging.error("Reconnection attempt %d failed: %s", attempt + 1, str(e))
                time.sleep(2)
        logging.error("Max reconnection attempts reached. Exiting.")
        raise SystemExit(1)
def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode("utf-8")
    try:
        dati_json = json.loads(payload)
    except json.JSONDecodeError:
        logging.error("Invalid payload from topic %s: %s", topic, payload)
        return
    if topic.startswith("hospital/patient/"):
        tipo = "patient"
    elif topic.startswith("hospital/room/"):
        tipo = "room"
    elif topic.startswith("hospital/asset/"):
        tipo = "asset"
    else:
        logging.warning("Received message on unknown topic: %s", topic)
        return

    if dati_json is None:
        logging.error("dati non validi, messaggio scartato")
        return
    allarmi = []
    if tipo == "patient":
        if processor.validate_patient_data(dati_json):
            allarmi = processor.check_patient_alerts(dati_json)
            db.save_patient_data(dati_json)
            logging.info("Salvati dati paziente: %s", dati_json.get('patient_id'))
        else:
            logging.error("Dati paziente non validi: %s", dati_json)
            return
    elif tipo == "room":
        if processor.validate_room_data(dati_json):
            allarmi = processor.check_room_alerts(dati_json)
            db.save_room_data(dati_json)
            logging.info("Salvati dati stanza: %s", dati_json.get('room_id'))
        else:
            logging.error("Dati stanza non validi: %s", dati_json)
            return
    elif tipo == "asset":
        if processor.validate_asset_data(dati_json):
            allarmi = processor.check_asset_alerts(dati_json)
            db.save_asset_data(dati_json)
            logging.info("Salvati dati asset: %s", dati_json.get('asset_id'))
        else:
            logging.error("Dati asset non validi: %s", dati_json)
            return
    for allarme in allarmi:
        db.save_alert(allarme)
        logging.warning("Allarme salvato: %s", allarme)
    
    logging.info("ricevuto messaggio su topic %s: %s", topic, payload)
def start_mqtt_client():
    try :
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_disconnect = on_disconnect
        client.on_message = on_message
        client.connect(BROKER, PORT, 60)
        client.loop_start()
        logging.info("mqtt subscriber attivo e in ascolto...")
        while True:
            time.sleep(1)
    except Exception as e:
        logging.error("error connessione iniziale al broker: %s", str(e))
def stop_mqtt_client(client):
    client.loop_stop()
    client.disconnect()
    logging.info("mqtt subscriber disconnesso e fermato")
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    start_mqtt_client()

