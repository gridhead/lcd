#! /usr/bin/env python

# Custom characters string program for 20x4 LCD. Writes strings with custom characters, that can't
# be found in the characters table. It is possible to use a custom characters by defining
# it's code on placeholder while using and extended string.
# Appearance of the custom characters can be defined by redefinition of the fields of
# CustomCharacters class instance.
# Codes of the custom characters, that can be used in placeholders are the following:
# 1st - {0x00}, 2nd - {0x01}, 3rd - {0x02}, 4th - {0x03}, 5th - {0x04},
# 6th - {0x05}, 7th - {0x06} and 8th - {0x07}
# Remember to use method load_custom_characters_data() to load the custom characters
# data into the CG RAM.
# Demo program for the I2C 20x4 Display
# Based on the original by Dmitry Safonov

# Import necessary libraries for communication and display use
import drivers
from time import sleep

# Load the driver and set it to "display" for 20x4 LCD
# If you use something from the driver library use the "display." prefix first
display = drivers.Lcd(cols=20, rows=4)

# Create object with custom characters data
cc = drivers.CustomCharacters(display)

# Redefine the default characters:
# Custom character #1. Code {0x00}.
cc.char_1_data = ["01110",
                  "01010",
                  "01110",
                  "00100",
                  "11111",
                  "11111",
                  "11111",
                  "11111"]

# Custom character #2. Code {0x01}.
cc.char_2_data = ["11111",
                  "10101",
                  "10101",
                  "11111",
                  "11111",
                  "10101",
                  "10101",
                  "11111"]

# Custom character #3. Code {0x02}.
cc.char_3_data = ["10001",
                  "10001",
                  "10001",
                  "11111",
                  "11111",
                  "11111",
                  "11111",
                  "11111"]

# Custom character #4. Code {0x03}.
cc.char_4_data = ["11111",
                  "11011",
                  "10001",
                  "10001",
                  "10001",
                  "10001",
                  "11011",
                  "11111"]

# Custom character #5. Code {0x04}.
cc.char_5_data = ["00000",
                  "00000",
                  "11011",
                  "11011",
                  "00000",
                  "10001",
                  "01110",
                  "00000"]

# Custom character #6. Code {0x05}.
cc.char_6_data = ["01010",
                  "11111",
                  "11111",
                  "01110",
                  "00100",
                  "00000",
                  "00000",
                  "00000"]

# Custom character #7. Code {0x06}.
cc.char_7_data = ["11111",
                  "11011",
                  "10001",
                  "10101",
                  "10101",
                  "10101",
                  "11011",
                  "11111"]

# Custom character #8. Code {0x07}.
cc.char_8_data = ["11111",
                  "10001",
                  "11111",
                  "00000",
                  "00000",
                  "11111",
                  "10001",
                  "11111"]
# Load custom characters data to CG RAM:
cc.load_custom_characters_data()

# Main body of code
try:
    while True:
        # Remember that your sentences can only be 20 characters long on a 20x4 display!
        print("Printing custom characters:")
        display.lcd_display_string("Custom characters:", 1)  # Write line of text to first line of display
        display.lcd_display_extended_string("All 8:{0x00}{0x01}{0x02}{0x03}{0x04}{0x05}{0x06}{0x07}", 2)  # Write line of text to second line of display
        display.lcd_display_string("20x4 LCD Demo", 3)  # Third line
        display.lcd_display_string("Pretty cool, right?", 4)  # Fourth line
        sleep(2) # Give time for the message to be read
except KeyboardInterrupt:
    # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup
    print("Cleaning up!")
    display.lcd_clear()
