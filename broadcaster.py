import socket 
import time
import json

BROADCAST_IP = "255.255.255.255"
PORT = 5005

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    finally:
        s.close()

local_ip = get_local_ip()

message = json.dumps({
    "ip": local_ip,
    "mqttPort": 1883,
    "wsPort": 9001,
    "httpPort": 8000
})

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

while True:
    sock.sendto(message.encode(), (BROADCAST_IP, PORT))
    print(f"Broadcasted: {message}")
    time.sleep(5)