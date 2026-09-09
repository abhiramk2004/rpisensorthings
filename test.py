import gpiod
import time
chip = gpiod.Chip('/dev/gpiochip4')
line = chip.get_line(4)
line.request(consumer="test", type=gpiod.LINE_REQ_DIR_IN)
while True:
    print(line.get_value())
    time.sleep(1)
