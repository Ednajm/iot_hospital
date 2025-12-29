import paho.mqtt.client as mqtt
import json 
import time 
import random 

client = mqtt.Client()
client.connect("localhost", 1883)
departaments = ["lab_id" ,"ICU_id", "emergency_id", "room_id"]

asset_ids = [f"asset_ids{i}" for i in range(1,200)]
def posizione_asset():
    return random.choice(departaments)
def stato_operativi():
    stati = ["active", "standby", "maintenance"]
    return random.choice(stati)
while True:
    for asset_id in asset_ids:
        data = {
            "asset_id": asset_id,
            "location": posizione_asset(),
            "status": stato_operativi(),
            "battery": random.randint(20, 100)
        }

        message = json.dumps(data)
        topic = f"hospital/asset/{asset_id}"
        client.publish(topic, message)

        print(f" Inviato -> Topic: {topic} | Dati: {message}")

    time.sleep(5)

    

