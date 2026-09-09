import time
import board
import adafruit_dht
import gpiozero as DigitalInputDevice
lt = DigitalInputDevice(17)
dht = adafruit_dht.DHT11(board.D4)
while True:
    try:
        temp = dht.temperature
        hum = dht.humidity
        lt = GPIO.input(17)
        light="bright"
        if(lt.value == 1):light="dark"
        print(
            f"Temp={temp}°C  Humidity={hum}%  Light={light}"
        )

    except RuntimeError:
        pass

    time.sleep(2)
