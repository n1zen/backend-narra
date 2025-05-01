import json
import time
import paho.mqtt.client as mqtt
from get_data import get_sensor_data

client = mqtt.Client()
client.connect("localhost", 1883, 60)

def publish_sensor_data():
    while True:
        # Fake sensor data
        sensor_data = {
            "humidity": 25.6,
            "temperature": 32.5,
            "ec": 102.5,
            "ph": 6.2
        }

        payload = json.dumps(sensor_data)
        client.publish("get_data", payload)
        print(f"Published: {payload}")
        time.sleep(5)  # publish every 5 seconds

        # actual sensor data
        # get_sensor_data(client)
        # time.sleep(5)

publish_sensor_data()