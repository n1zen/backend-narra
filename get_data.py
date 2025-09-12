import serial
# def get_sensor_data(mqtt_client):
def get_sensor_data(mqtt_client):
	ser = serial.Serial('/dev/ttyUSB0',9600,timeout=1)
	ser.reset_input_buffer()
	n = 1
	while(n == 1):
		if ser.in_waiting > 0:
			line = ser.readline().decode('utf-8').rstrip()
			mqtt_client.publish("get_data", line)
			print(line)
			n = n - 1
	ser.close()