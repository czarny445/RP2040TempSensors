import board
import busio
import json
import time
from rgblib import RGB_LCD

from adafruit_character_lcd.character_lcd_i2c import Character_LCD_I2C
from adafruit_onewire.bus import OneWireBus
from adafruit_ds18x20 import DS18X20
from adafruit_bus_device.i2c_device import I2CDevice
from adafruit_binascii import hexlify

# Set pins 8 and 9 to I2C mode
i2c = busio.I2C(board.GP9, board.GP8)

#Retrieve temperature from DS18B20 sensor on pin 16

ow_bus1 = OneWireBus(board.GP16)
ow_bus2 = OneWireBus(board.GP17)

# Scan for sensors and grab the first one found.
deviceIdsOnBus1 = ow_bus1.scan()
deviceIdsOnBus2 = ow_bus2.scan()

dsDevicesOnBus1 = []
dsDevicesOnBus2 = []

for i in deviceIdsOnBus1:
    dsDevicesOnBus1.append(DS18X20(ow_bus1, i))
for i in deviceIdsOnBus2:
    dsDevicesOnBus2.append(DS18X20(ow_bus2, i))


lcd = RGB_LCD(cols=16, lines=2, dotsize=8, wire=i2c)
lcd.clear()
lcd.home()

# Main loop to print the temperature every second.
while True:
    temperaturesMap = dict()
    lcd.clear()
    for i in range(len(dsDevicesOnBus1)):
        hexId = hexlify(deviceIdsOnBus1[i].rom)
        temperaturesMap[hexId] = dsDevicesOnBus1[i].temperature
        lcd.println("Temp1: {0:0.3f}C".format(temperaturesMap[hexId]))
        time.sleep(2)
    for i in range(len(dsDevicesOnBus2)):
        hexId = hexlify(deviceIdsOnBus2[i].rom)
        temperaturesMap[hexId] = dsDevicesOnBus2[i].temperature
        lcd.println("Temp2: {0:0.3f}C".format(temperaturesMap[hexId]))
        time.sleep(2)
    print(json.dumps(temperaturesMap))
    time.sleep(2)

