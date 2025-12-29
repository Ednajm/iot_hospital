import paho.mqtt.client as mqtt
import json 
import time 
import random
client = mqtt.Client()
client.connect("localhost", 1883)
patient_ids = []

def initialize_patients():
    size = 5000
    for i in range(size):
        patient_ids.append(i)
    return patient_ids
initialize_patients()
while True:
    selected_patient = random.choice(patient_ids) if patient_ids else 500
    
    data = {
        "patient_id": selected_patient,
        "heart_rate": random.randint(60, 120),
        "temperature": round(random.uniform(36, 39), 1),
        "spo2": random.randint(90, 100)
    }
    
    message = json.dumps(data)
    client.publish("hospital/patient/1", message)
    print("Inviato:", message)
    time.sleep(5) 