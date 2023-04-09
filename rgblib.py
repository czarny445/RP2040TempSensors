# Circutpython lib for non-RGB Grove - 16x2 LCD I2C display
# https://wiki.seeedstudio.com/Grove-16x2_LCD_Series/
# Working with v2.0 version of the display
# Rewrited from original library from seeedstudio
# Usage:
# lcd = RGB_LCD(cols=16, lines=2, dotsize=8, wire=i2c)
# lcd.clear()
# lcd.println("Hello World!")
# Verion: 0.1
# Author: @czarny445

import board
import busio
import time
import io
import re


LCD_ADDRESS = 0x3E
RGB_ADDRESS_V5 = 0x74
RGB_ADDRESS = 0x62
REG_MODE1 = 0x00
REG_OUTPUT = 0x08
REG_MODE2 = 0x01

# Define constants for the LCD commands
LCD_CLEARDISPLAY = 0x01
LCD_RETURNHOME = 0x02
LCD_ENTRYMODESET = 0x04
LCD_DISPLAYCONTROL = 0x08
LCD_CURSORSHIFT = 0x10
LCD_FUNCTIONSET = 0x20
LCD_SETCGRAMADDR = 0x40
LCD_SETDDRAMADDR = 0x80

# flags for display entry mode
LCD_ENTRYRIGHT = 0x00
LCD_ENTRYLEFT = 0x02
LCD_ENTRYSHIFTINCREMENT = 0x01
LCD_ENTRYSHIFTDECREMENT = 0x00

# Define constants for the display properties
LCD_DISPLAYON = 0x04
LCD_DISPLAYOFF = 0x00
LCD_CURSORON = 0x02
LCD_CURSOROFF = 0x00
LCD_BLINKON = 0x01
LCD_BLINKOFF = 0x00
LCD_ENTRYRIGHT = 0x00
LCD_ENTRYLEFT = 0x02
LCD_ENTRYSHIFTINCREMENT = 0x01
LCD_ENTRYSHIFTDECREMENT = 0x00
LCD_DISPLAYMOVE = 0x08
LCD_CURSORMOVE = 0x00
LCD_MOVERIGHT = 0x04
LCD_MOVELEFT = 0x00


# flags for function set
LCD_8BITMODE = 0x10
LCD_4BITMODE = 0x00
LCD_2LINE = 0x08
LCD_1LINE = 0x00
LCD_5x10DOTS = 0x04
LCD_5x8DOTS = 0x00

class RGB_LCD:
    def __init__(self, cols, lines, dotsize, wire):
        """ Contructor for Screen interface. Use it once to initaite the LCD. """
        self._wire = wire
        self._cols = cols
        self._lines = lines
        self._dotsize = dotsize
        self._displayfunction = 0
        self._displaycontrol = 0
        self._displaymode = 0
        self._initialized = 0
        self._numlines = 0
        self._newLineRegEx = re.compile("[\r\n]")

        
        while not self._wire.try_lock():
	        time.sleep(0.5)

        if lines > 1:
            self._displayfunction |= LCD_2LINE
        self._numlines = lines
        self._currline = 0

        # for some 1 line displays you can select a 10 pixel high font
        if dotsize != 0 and lines == 1:
            self._displayfunction |= LCD_5x10DOTS

        # SEE PAGE 45/46 FOR INITIALIZATION SPECIFICATION!
        # according to datasheet, we need at least 40ms after power rises above 2.7V
        # before sending commands. Arduino can turn on way befer 4.5V so we'll wait 50
        time.sleep(0.05)

        # this is according to the hitachi HD44780 datasheet
        # page 45 figure 23

        # Send function set command sequence
        self.command(LCD_FUNCTIONSET | self._displayfunction)
        time.sleep(0.0045)  # wait more than 4.1ms

        # second try
        self.command(LCD_FUNCTIONSET | self._displayfunction)
        time.sleep(0.00015)

        # third go
        self.command(LCD_FUNCTIONSET | self._displayfunction)

        # finally, set # lines, font size, etc.
        self.command(LCD_FUNCTIONSET | self._displayfunction)

        # turn the display on with no cursor or blinking default
        self._displaycontrol = LCD_DISPLAYON | LCD_CURSOROFF | LCD_BLINKOFF
        self.display()

        # clear it off
        self.clear()

        # Initialize to default text direction (for romance languages)
        self._displaymode = LCD_ENTRYLEFT | LCD_ENTRYSHIFTDECREMENT
        # set the entry mode
        self.command(LCD_ENTRYMODESET | self._displaymode)
    def __i2c_send_bytes(self, dta):
        self._wire.writeto(LCD_ADDRESS, dta)
        
    def command(self, value):
        dta = bytearray([0x80, value])
        self.__i2c_send_bytes(dta)
    def __write(self, value):
        """ Writes a string to the LCD. """
        dta = bytearray([0x40])
        dta.extend(value.encode('ascii'))
        self.__i2c_send_bytes(dta)
        return 1 # assume success 
    def __writeWithEndlines(self, value):
        """ Prints a string to the LCD. Gets \r\n \r and \n as a line break. """
        lines = self._newLineRegEx.split(value)
        for line in lines:            
            if line != "":
                self.__write(line)
                if len(lines) > 1:
                    self._currline = (self._currline + 1) % self._numlines
                    self.setCursor(0, self._currline)
                

            
    def print(self, value):
        """ Prints a string to the LCD."""
        self.__writeWithEndlines(value)
    def println(self, value):
        """ Prints a string to the LCD with endline"""
        self.__writeWithEndlines(value + "\r")
    def clear(self):
        """ Clears the LCD screen. """
        self.command(LCD_CLEARDISPLAY)
        time.sleep(0.002) # wait for 2 milliseconds
    def home(self):
        """ Sets the cursor to the home position. """
        self.command(LCD_RETURNHOME)
        time.sleep(0.002) # this command takes a long time!
    def no_display(self):
        """ Turns off the LCD display. """
        self._displaycontrol &= ~LCD_DISPLAYON
        self.command(LCD_DISPLAYCONTROL | self._displaycontrol)
    def display(self):
        """ Turns on the LCD display. """
        self._displaycontrol |= LCD_DISPLAYON
        self.command(LCD_DISPLAYCONTROL | self._displaycontrol)
    def no_cursor(self):
        """ Turns off the LCD cursor. """
        self._displaycontrol &= ~LCD_CURSORON
        self.command(LCD_DISPLAYCONTROL | self._displaycontrol)
    def cursor(self):
        """ Turns on the LCD cursor. """
        self._displaycontrol |= LCD_CURSORON
        self.command(LCD_DISPLAYCONTROL | self._displaycontrol)
    def no_blink(self):
        """ Turns off the LCD blinking cursor. """
        self._displaycontrol &= ~LCD_BLINKON
        self.command(LCD_DISPLAYCONTROL | self._displaycontrol)
    def blink(self):
        """ Turns on the LCD blinking cursor. """
        self._displaycontrol |= LCD_BLINKON
        self.command(LCD_DISPLAYCONTROL | self._displaycontrol)
    def setCursor(self, col, row):
        """ Sets the cursor position. """
        col = col | (0x80 if row == 0 else 0xc0)
        dta = bytearray([0x80, col])
        self.__i2c_send_bytes(dta)
    