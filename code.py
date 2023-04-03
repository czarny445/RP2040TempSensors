import board
import busio
import time
from rgblib import RGB_LCD

from adafruit_character_lcd.character_lcd_i2c import Character_LCD_I2C
from adafruit_onewire.bus import OneWireBus
from adafruit_ds18x20 import DS18X20
from adafruit_bus_device.i2c_device import I2CDevice


# Set pins 8 and 9 to I2C mode
i2c = busio.I2C(board.GP9, board.GP8)

#Retrieve temperature from DS18B20 sensor on pin 16

ow_bus1 = OneWireBus(board.GP16)
ow_bus2 = OneWireBus(board.GP17)

# Scan for sensors and grab the first one found.
ds18x1 = DS18X20(ow_bus1, ow_bus1.scan()[0])
ds18x2 = DS18X20(ow_bus1, ow_bus1.scan()[1])
ds18x3 = DS18X20(ow_bus2, ow_bus2.scan()[0])
ds18x4 = DS18X20(ow_bus2, ow_bus2.scan()[1])


lcd = RGB_LCD(cols=16, lines=2, dotsize=8, wire=i2c)
lcd.clear()
lcd.cursor()

# Main loop to print the temperature every second.
while True:
    a = ds18x1.temperature;
    b = ds18x2.temperature;
    c = ds18x3.temperature;
    d = ds18x4.temperature;
    lcd.clear()
    lcd.println("Temp1: {0:0.3f}C".format(a))
    time.sleep(5.0)

    lcd.println("Temp2: {0:0.3f}C".format(b))
    time.sleep(5.0)
    lcd.clear()
    lcd.println("Temp3: {0:0.3f}C".format(c))
    time.sleep(5.0)

    lcd.println("Temp4: {0:0.3f}C".format(d))
    time.sleep(3.0)
    lcd.setCursor(8, 1)
    time.sleep(3.0)
    lcd.setCursor(8, 0)
    time.sleep(3.0)
    lcd.setCursor(8, 1)
    time.sleep(3.0)
    lcd.setCursor(8, 0)




