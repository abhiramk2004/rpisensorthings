import time
while True:
    for _ in range(5):
        try:
           with open("/sys/bus/iio/devices/iio:device0/in_temp_input","rt") as f:
              temp = int(f.readline().strip())/1000
           with open("/sys/bus/iio/devices/iio:device0/in_humidityrelative_input","rt") as f:
              hum = int(f.readline().strip())/1000
           print(f"temp:{temp} hum:{hum}")
           break
        except OSError:
           time.sleep(1)
    time.sleep(5)
