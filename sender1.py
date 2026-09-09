# Import the 'socket' module.
# This allows the Raspberry Pi to communicate with other devices over a network.
import socket

# Import the 'json' module.
# JSON is a simple text format used to structure data so that different programs
# and devices can easily understand and exchange it.
import json

# Import the 'time' module.
# We will use it to get the current time and to pause the program between readings.
import time

# Import the 'board' module from CircuitPython.
# It provides names for the physical GPIO pins on the Raspberry Pi.
import board

# Import the Adafruit DHT library.
# This library allows Python to communicate with DHT-series temperature/humidity sensors.
import adafruit_dht

# Import the Raspberry Pi GPIO library.
# GPIO stands for General Purpose Input/Output and lets Python read signals
# from physical pins on the Raspberry Pi.
import RPi.GPIO as GPIO


# --------------------------------------------------
# Sensor Setup
# --------------------------------------------------

# Tell the GPIO library that we want to refer to pins using their BCM numbers.
# BCM = Broadcom GPIO numbering used by the Raspberry Pi internally.
GPIO.setmode(GPIO.BCM)

# Configure GPIO pin 17 as an INPUT.
# An input pin is used to read a signal coming from an external sensor.
GPIO.setup(17, GPIO.IN)

# Create a DHT11 sensor object.
# board.D4 means the DHT11 data pin is connected to GPIO 4 on the Raspberry Pi.
# The variable 'dht' will now represent our DHT11 sensor in the program.
dht = adafruit_dht.DHT11(board.D4)


# --------------------------------------------------
# UDP Setup
# --------------------------------------------------

# IP address of the device that should receive our sensor data.
# Here, the Raspberry Pi will send the data to the device with this IP address.
TARGET_IP = "10.42.0.1"

# Port number on the receiving device where the data should be sent.
# The receiving program must be listening on this same port.
TARGET_PORT = 5000

# Create a network socket.
#
# AF_INET  -> use IPv4 addresses.
# SOCK_DGRAM -> use UDP communication.
#
# UDP sends independent packets of data without establishing a connection first.
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Display a message so we know where the Raspberry Pi is sending the data.
print(f"Sending UDP packets to {TARGET_IP}:{TARGET_PORT}")


# --------------------------------------------------
# Main Loop
# --------------------------------------------------

# 'while True' creates an infinite loop.
# Everything inside this loop will continuously execute until the program is stopped.
while True:

    # 'try' allows us to run code that might produce an error.
    # If an error occurs, the program can handle it instead of immediately crashing.
    try:

        # Read the current temperature from the DHT11 sensor.
        # The value is usually returned in degrees Celsius.
        temp = dht.temperature

        # Read the current relative humidity from the DHT11 sensor.
        # The value is returned as a percentage.
        hum = dht.humidity

        # Read the electrical signal on GPIO pin 17.
        #
        # GPIO.input(17) returns:
        #     0 -> LOW signal
        #     1 -> HIGH signal
        #
        # Here, this value represents the state of the light sensor.
        light = GPIO.input(17)


        # Create a Python dictionary containing all the sensor information.
        #
        # A dictionary stores data as key-value pairs.
        # For example:
        #     "temperature": 25
        #
        # means the key "temperature" has the value 25.
        packet = {

            # Name/identifier of this sensor node.
            # This helps the receiver know which device sent the data.
            "node": "sensor_pi",

            # Get the current Unix timestamp.
            #
            # time.time() gives the current time as the number of seconds
            # since January 1, 1970 (Unix epoch).
            #
            # int() removes the decimal part.
            "timestamp": int(time.time()),

            # Store the temperature measured by the DHT11.
            "temperature": temp,

            # Store the humidity measured by the DHT11.
            "humidity": hum,

            # Store the light sensor's digital value (0 or 1).
            "light": light
        }


        # Convert the Python dictionary into a JSON string.
        #
        # Python understands dictionaries, but when sending data over a network,
        # we need to convert the dictionary into a standard data format.
        #
        # json.dumps(packet)
        #     -> converts the dictionary into JSON text.
        #
        # .encode()
        #     -> converts the text into bytes because sockets send bytes,
        #        not normal Python strings.
        data = json.dumps(packet).encode()


        # Send the JSON data to the target device using UDP.
        #
        # sendto() takes two arguments:
        #
        # 1. data
        #    -> the actual bytes we want to send.
        #
        # 2. (TARGET_IP, TARGET_PORT)
        #    -> the destination IP address and port.
        #
        # Unlike TCP, UDP does not require us to establish a connection first.
        sock.sendto(data, (TARGET_IP, TARGET_PORT))


        # Print the dictionary to the Raspberry Pi's terminal.
        # This lets us see what data is being sent.
        print(packet)


    # DHT11 sensors can occasionally fail to provide a valid reading.
    # For example, a checksum error can occur because of timing/noise.
    #
    # RuntimeError catches these expected sensor-reading errors.
    # Instead of stopping the entire program, we simply print the error
    # and allow the loop to continue.
    except RuntimeError as e:

        # Print the error message.
        # 'e' contains information about what went wrong.
        print(f"DHT11 Error: {e}")


    # Catch any other type of unexpected error.
    #
    # Exception is a general error type, so this prevents many other
    # problems from completely terminating the program.
    except Exception as e:

        # Print the error so we can diagnose what went wrong.
        print(f"Error: {e}")


    # Pause the program for 1 second before taking the next sensor reading.
    #
    # Without this delay, the loop would run as fast as possible,
    # continuously reading the sensor and sending packets.
    time.sleep(1)
