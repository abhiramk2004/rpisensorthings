#!/usr/bin/env python

from smbus import SMBus
import time

def main():
    '''
    Main program function
    '''

    i2cbus = SMBus(1)  # Create a new I2C bus
    i2caddress = 0x18  # Address of Max9867 device
    i2cbus.write_byte_data(i2caddress, 0x17, 0x0A)
    i2cbus.write_byte_data(i2caddress, 0x04, 0x00)
    i2cbus.write_byte_data(i2caddress, 0x05, 0x10)
    i2cbus.write_byte_data(i2caddress, 0x06, 0xD8)
    i2cbus.write_byte_data(i2caddress, 0x07, 0x33)
    i2cbus.write_byte_data(i2caddress, 0x08, 0x18)
    i2cbus.write_byte_data(i2caddress, 0x09, 0x0A)
    i2cbus.write_byte_data(i2caddress, 0x0A, 0x91)
    i2cbus.write_byte_data(i2caddress, 0x0B, 0x00)
    i2cbus.write_byte_data(i2caddress, 0x0C, 0x00)
    i2cbus.write_byte_data(i2caddress, 0x0D, 0x00)
    i2cbus.write_byte_data(i2caddress, 0x0E, 0x40)
    i2cbus.write_byte_data(i2caddress, 0x0F, 0x40)
    i2cbus.write_byte_data(i2caddress, 0x10, 0x09)
    i2cbus.write_byte_data(i2caddress, 0x11, 0x09)
    i2cbus.write_byte_data(i2caddress, 0x12, 0x24)
    i2cbus.write_byte_data(i2caddress, 0x13, 0x24)
    i2cbus.write_byte_data(i2caddress, 0x14, 0x50)
    i2cbus.write_byte_data(i2caddress, 0x15, 0x00)
    i2cbus.write_byte_data(i2caddress, 0x16, 0x60)
    i2cbus.write_byte_data(i2caddress, 0x17, 0x8A)
    print1 = i2cbus.read_byte_data(0x18, 0x0A)
    print2 = i2cbus.read_byte_data(0x18, 0x12)
    print3 = i2cbus.read_byte_data(0x18, 0x06)
    print(' ')
    print(print1)
    print(' ')
    print(print2)
    print(' ')
    print(print3)

if __name__ == "__main__":
    main()
