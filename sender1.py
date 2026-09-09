import socket
import json
import time
import board
import adafruit_dht
import RPi.GPIO as GPIO

# -----------------------------
# Sensor Setup
# -----------------------------
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)

dht = adafruit_dht.DHT11(board.D4)

# -----------------------------
# UDP Setup
# -----------------------------
TARGET_IP = "10.42.0.1"
TARGET_PORT = 5000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print(f"Sending UDP packets to {TARGET_IP}:{TARGET_PORT}")

# -----------------------------
# Main Loop
# -----------------------------
while True:
    try:
        temp = dht.temperature
        hum = dht.humidity
        light = GPIO.input(17)

        packet = {
            "node": "sensor_pi",
            "timestamp": int(time.time()),
            "temperature": temp,
            "humidity": hum,
            "light": light
        }

        data = json.dumps(packet).encode()

        sock.sendto(data, (TARGET_IP, TARGET_PORT))

        print(packet)

    except RuntimeError as e:
        # DHT11 occasionally throws checksum/read errors
        print(f"DHT11 Error: {e}")

    except Exception as e:
        print(f"Error: {e}")

    time.sleep(1)
