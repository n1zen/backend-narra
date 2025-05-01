import json
import time
import paho.mqtt.client as mqtt
from get_data import get_sensor_data
import random

client = mqtt.Client()
client.connect("localhost", 1883, 60)

list_of_moisture = [25.6, 21.6, 60.25, 100, 52.2]
list_of_temperature = [29.3, 35.3, 51.3, 25.3, 15.6]
list_of_ec = [102.5, 512.36, 215.32, 78.3, 124.53]
list_of_ph = [3, 4, 5, 6, 7, 8]

def publish_sensor_data():
    while True:
        # Fake sensor data
        sensor_data = {
            "Moist": random.choice(list_of_moisture),
            "Temp": random.choice(list_of_temperature),
            "EC": random.choice(list_of_ec),
            "pH": random.choice(list_of_ph)
        }
        payload = json.dumps(sensor_data)
        client.publish("get_data", payload)
        print(f"Published: {payload}")
        time.sleep(3)  # publish every 5 seconds

        # actual sensor data
        # get_sensor_data(client)
        # time.sleep(5)

publish_sensor_data()