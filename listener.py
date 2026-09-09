import socket
import json
import time
LISTEN_IP = "0.0.0.0"
LISTEN_PORT = 5000
MEC_IP = "192.168.10.12"
PORT = 5000
rx_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
rx_sock.bind((LISTEN_IP, LISTEN_PORT))
tx_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print(f"Listening on UDP {LISTEN_IP}:{LISTEN_PORT}")
while True:
    data, addr = rx_sock.recvfrom(4096)

    try:
        message = json.loads(data.decode())
        print(message)
        tx_sock.sendto(data,(MEC_IP,PORT))
        print("forwarded")
    except Exception as e:
        print(f"\nReceived non-JSON data from {addr}")
        print(data)
        print(f"Error: {e}")
        time.sleep(1)
