import paho.mqtt.client as mqtt
import logging 
import time 
import json 
import signal
import data_processor
import database 
import configparser
Let_config = {"broker": "mqtt.dashboard.link"}
port = {"port": 1883}
topic = {"hospital/patient/+","hospital/room/+","hospital/asset/+"}
qos = configparser.get("MQTT", "qos", fallback=1)
reconnect_max_retry = configparser.get("MQTT", "reconnect_max_retry", fallback=5)
def _init_():
    client = mqtt.client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    def data_handler(data):
        data_processor.process_data(data)
    def database_handler(data):
        database.store_data(data)
    logging.info("Connecting to MQTT broker at %s:%s", Let_config["broker"], port["port"])
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            logging.info("Connected to MQTT broker")
            for t in topic:
                client.subscribe(t, qos)
                logging.info("Subscribed to topic: %s", t)
        else:
            logging.error("Failed to connect, return code %d", rc)
    def on_disconnect(client, userdata, rc):
        if rc != 0:
            logging.warning("Unexpected disconnection. Attempting to reconnect...")
            for attempt in range(reconnect_max_retry):
                try:
                    client.reconnect()
                    logging.info("Reconnected to MQTT broker")
                    return
                except Exception as e:
                    logging.error("Reconnection attempt %d failed: %s", attempt + 1, str(e))
                    time.sleep(2)
            logging.error("Max reconnection attempts reached. Exiting.")
            exit(1)
    def on_message(client, userdata, msg):
        topic = msg.topic
        payload = msg.payload.decode('utf-8')
        try:
            dati_json = JSON.parse(payload_bytes.decode('utf-8'))
        else: 
            log("playload non valido da topic : %s", payload)
            return
    if patient in topic:
        tipo = "patient"
    print("patient_id", "heart_rate", "spo2", "temperature", "timestamp")
    elif room in topic:
       tipo = "room"
       print("room_id", "temperature", "humidity", "co2", "timestamp")
    elif asset in topic:
       tipo = "asset"
       print("asset_id", "status", "battery_level", "timestamp")
    if dati  

