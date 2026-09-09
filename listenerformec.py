import socket
import json


# --------------------------------------------------
# UDP Receiver Setup
# --------------------------------------------------

# IP address to listen on.
#
# "0.0.0.0" means:
# Listen for UDP packets arriving on ANY network interface
# of the MEC machine.
#
# This is useful because we don't need to know in advance
# which network interface the packets will arrive through.
LISTEN_IP = "0.0.0.0"


# UDP port on which the MEC will listen.
#
# This MUST match the destination port used by the
# forwarding device.
#
# In your previous code:
#     PORT = 5000
#
# Therefore, the MEC also listens on port 5000.
LISTEN_PORT = 5000


# --------------------------------------------------
# Create UDP Socket
# --------------------------------------------------

# Create a socket for UDP communication.
#
# AF_INET:
#     Use IPv4 addresses.
#
# SOCK_DGRAM:
#     Use UDP.
#
# This socket will be responsible for receiving
# packets from the forwarding device.
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


# --------------------------------------------------
# Bind Socket
# --------------------------------------------------

# Bind the socket to the IP address and port.
#
# This tells the operating system:
#
#     "Whenever a UDP packet arrives on port 5000,
#      give it to this Python program."
#
# Since we use 0.0.0.0, packets arriving through
# any network interface can be received.
sock.bind((LISTEN_IP, LISTEN_PORT))


# Print a message so we know that the MEC is ready
# and waiting for incoming packets.
print(f"Listening for UDP packets on {LISTEN_IP}:{LISTEN_PORT}")


# --------------------------------------------------
# Main Receiving Loop
# --------------------------------------------------

# Keep receiving packets forever.
#
# The loop will continue until the program is manually
# stopped, for example with Ctrl+C.
while True:

    # Wait for a UDP packet to arrive.
    #
    # recvfrom(4096) means:
    #
    #     Receive a maximum of 4096 bytes.
    #
    # It returns two values:
    #
    #     data -> the actual bytes received
    #     addr -> IP address and port of the sender
    #
    # This is a blocking call, meaning Python will wait
    # here until a packet arrives.
    data, addr = sock.recvfrom(4096)


    # --------------------------------------------------
    # Process Received Data
    # --------------------------------------------------

    try:

        # Convert the received bytes into a string.
        #
        # Network sockets give us bytes, while JSON is
        # normally represented as text.
        #
        # Example:
        #
        #     b'{"temperature":25,"humidity":60}'
        #
        # becomes:
        #
        #     '{"temperature":25,"humidity":60}'
        text = data.decode()


        # Convert the JSON string into a Python object.
        #
        # If the sender sent a JSON dictionary such as:
        #
        #     {
        #         "node": "sensor_pi",
        #         "temperature": 25,
        #         "humidity": 60,
        #         "light": 1
        #     }
        #
        # json.loads() converts it into a Python dictionary.
        message = json.loads(text)


        # Print the address of the device that sent the packet.
        print(f"\nReceived packet from {addr}")


        # Print the decoded sensor data.
        print("Sensor data:")
        print(message)


    # If the received packet is not valid JSON,
    # or if some other processing error occurs,
    # handle the error here instead of crashing.
    except Exception as e:

        # Tell us that something went wrong while
        # processing the received packet.
        print(f"\nError processing packet from {addr}: {e}")


        # Print the raw data so we can see exactly
        # what was received.
        print("Raw data:")
        print(data)
