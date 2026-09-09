from gpiozero import DigitalInputDevice
import time
ldr = DigitalInputDevice(4)
while True:
    print(ldr.value)
    time.sleep(2)
