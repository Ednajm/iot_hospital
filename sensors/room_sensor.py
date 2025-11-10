import paho.mqtt.client as mqtt
import json
import time
import random

client = mqtt.Client()
client.connect("localhost", 1883)

rooms = [f"Room{i}" for i in range(1, 501)]

print(f" Sensori ambiente attivi: {len(rooms)} stanze inizializzate ")
print("Connessione al broker MQTT riuscita \n")


while True:
    for room in rooms:
        
        temperature = round(random.uniform(20.0, 30.0), 1)   # °C
        humidity = random.randint(30, 70)                    # %
        co2 = random.randint(300, 1000)                      # ppm
        data = {
            "room_id": room,
            "temperature": temperature,
            "humidity": humidity,
            "co2": co2
        }

        message = json.dumps(data)
        topic = f"hospital/room/{room}"
        client.publish(topic, message)

        print(f"Inviato -> Topic: {topic} | Dati: {message}")

    
    time.sleep(7)
