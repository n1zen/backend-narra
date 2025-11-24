import json
import time
import paho.mqtt.client as mqtt
from get_data import get_sensor_data
import random

client = mqtt.Client()
client.connect("localhost", 1883, 60)

def publish_sensor_data():
    while True:
        # Fake sensor data
        # sensor_data = {
        #    "Moist": round(random.uniform(0, 100), 2),
        #    "Temp": round(random.uniform(-40, 80), 2),
        #    "EC": round(random.uniform(0, 20000), 2),
        #    "pH": round(random.uniform(3, 9), 1),
        #    "nitrogen": round(random.uniform(1, 2999), 2),
        #    "phosphorus": round(random.uniform(1, 2999), 2),
        #    "potassium": round(random.uniform(1, 2999), 2),
        # }
        # payload = json.dumps(sensor_data)
        # client.publish("get_data", payload)
        # print(f"Published: {payload}")
        # time.sleep(3)  # publish every 5 seconds

        # actual sensor data
        get_sensor_data(client)
        time.sleep(3)

publish_sensor_data()
