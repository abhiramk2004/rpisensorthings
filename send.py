import socket
import json
import time

# MEC details

TARGET_IP = "192.168.10.12"
TARGET_PORT = 5000

# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    data = {
        "node": "pi1",
        "message": "hello",
        "timestamp": time.time()
    }

    packet = json.dumps(data).encode()

    sock.sendto(packet, (TARGET_IP, TARGET_PORT))

    print(f"Sent: {data}")

    time.sleep(1)

