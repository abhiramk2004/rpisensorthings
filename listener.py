# Import the 'socket' module.
# It allows Python to communicate with other devices over a network.
import socket

# Import the 'json' module.
# JSON is used to convert structured data between Python and other programs.
import json

# Import the 'time' module.
# We use it to pause the program if an error occurs.
import time


# --------------------------------------------------
# Receiver / Listening Setup
# --------------------------------------------------

# IP address on which this program should listen for incoming UDP packets.
#
# "0.0.0.0" means:
#     Listen on ALL network interfaces of this computer.
#
# This allows the program to receive packets regardless of which
# network interface they arrive through.
LISTEN_IP = "0.0.0.0"

# UDP port on which we will listen for incoming packets.
#
# The sender (for example, the Raspberry Pi) must send its packets
# to this port.
LISTEN_PORT = 5000


# --------------------------------------------------
# MEC / Forwarding Setup
# --------------------------------------------------

# IP address of the MEC device to which received packets
# should be forwarded.
MEC_IP = "192.168.10.12"

# UDP port on the MEC device where the forwarded packets
# should be sent.
PORT = 5000


# --------------------------------------------------
# Create Receiving Socket
# --------------------------------------------------

# Create a UDP socket for receiving data.
#
# AF_INET:
#     Use IPv4 networking.
#
# SOCK_DGRAM:
#     Use UDP communication.
#
# This socket will be used only for receiving packets.
rx_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


# Bind the receiving socket to the specified IP address and port.
#
# bind() tells the operating system:
#
#     "Give incoming UDP packets arriving at port 5000
#      to this Python program."
#
# Since LISTEN_IP is "0.0.0.0", packets arriving on any
# network interface can be received.
rx_sock.bind((LISTEN_IP, LISTEN_PORT))


# --------------------------------------------------
# Create Transmitting Socket
# --------------------------------------------------

# Create another UDP socket.
#
# This socket will be used to SEND the received data
# to the MEC device.
tx_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


# Print a message so we know that the program has successfully
# started listening for incoming packets.
print(f"Listening on UDP {LISTEN_IP}:{LISTEN_PORT}")


# --------------------------------------------------
# Main Loop
# --------------------------------------------------

# Run the receiver continuously.
# The program will keep receiving and forwarding packets
# until it is manually stopped.
while True:

    # Wait until a UDP packet arrives.
    #
    # recvfrom(4096) means:
    #
    #     Read up to 4096 bytes from the incoming packet.
    #
    # It returns two things:
    #
    #     data -> the actual bytes received
    #     addr -> the sender's IP address and port
    #
    # This function is blocking, meaning the program will
    # wait here until a packet arrives.
    data, addr = rx_sock.recvfrom(4096)


    # Try to process the received packet.
    # If something goes wrong, the 'except' block below
    # will handle the error instead of crashing the program.
    try:

        # Convert the received bytes into a normal string.
        #
        # data is received as bytes, for example:
        #
        #     b'{"temperature":25,"humidity":60}'
        #
        # .decode() converts those bytes into text.
        message = json.loads(data.decode())


        # Convert the JSON text into a Python object.
        #
        # For example:
        #
        #     '{"temperature":25}'
        #
        # becomes:
        #
        #     {"temperature": 25}
        #
        # which is a Python dictionary.
        #
        # Then print the resulting Python object.
        print(message)


        # Forward the ORIGINAL received data to the MEC device.
        #
        # Notice that we use 'data' rather than 'message'.
        #
        # 'data' is still the original JSON bytes that were received.
        #
        # The packet is sent using UDP to:
        #
        #     MEC_IP = 192.168.10.12
        #     PORT   = 5000
        tx_sock.sendto(data, (MEC_IP, PORT))


        # Tell us that forwarding was successful.
        print("forwarded")


    # If anything inside the 'try' block causes an error,
    # execution comes here.
    #
    # For example:
    #
    #     - Received data isn't valid JSON
    #     - Data can't be decoded
    #     - Some other unexpected error occurs
    #
    # 'e' contains information about the error.
    except Exception as e:

        # Print a message saying that the received packet
        # wasn't valid JSON.
        #
        # '\n' adds an empty line before the message to make
        # the terminal output easier to read.
        print(f"\nReceived non-JSON data from {addr}")


        # Print the raw bytes that were received.
        #
        # This is useful for debugging because we can see
        # exactly what arrived over the network.
        print(data)


        # Print the actual error message.
        print(f"Error: {e}")


        # Wait for one second before continuing.
        #
        # This prevents the program from immediately processing
        # errors in a tight loop if something unusual happens.
        time.sleep(1)
