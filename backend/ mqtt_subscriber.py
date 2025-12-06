import paho.mqtt.client as mqtt
import logging
import time
import json
import data_processor
import database
import configparser
import csv

# Load configuration (falls back to sensible defaults)
_config = configparser.ConfigParser()
_config.read("config.ini")
MQTT_CONFIG = {
    "broker": _config.get("MQTT", "broker", fallback="mqtt.dashboard.link")
}
PORT = _config.getint("MQTT", "port", fallback=1883)
TOPICS = [
    "hospital/patient/+",
    "hospital/room/+",
    "hospital/asset/+",
]
QOS = _config.getint("MQTT", "qos", fallback=1)
RECONNECT_MAX_RETRY = _config.getint("MQTT", "reconnect_max_retry", fallback=5)
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

    # Determine message type from topic
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

    # Analyse data and store it
    allarmi = data_processor.analyse(tipo, dati_json)
    if allarmi:
        for allarme in allarmi:
            logging.warning("Allarme rilevato: %s", allarme)
    database.save(tipo, dati_json, allarmi)
    logging.info("ricevuto messaggio su topic %s: %s", topic, payload)
def start_mqtt_client():
    try :
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_disconnect = on_disconnect
        client.on_message = on_message
        client.connect(MQTT_CONFIG["broker"], PORT, 60)
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

