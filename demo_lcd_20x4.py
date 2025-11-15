#! /usr/bin/env python

# Simple string program for 20x4 LCD. Writes and updates strings.
# Demo program for the I2C 20x4 Display
# Based on the original by Matthew Timmons-Brown for The Raspberry Pi Guy YouTube channel

# Import necessary libraries for communication and display use
import drivers
from time import sleep

# Load the driver and set it to "display" for 20x4 LCD
# If you use something from the driver library use the "display." prefix first
display = drivers.Lcd(cols=20, rows=4)

# Main body of code
try:
    while True:
        # Remember that your sentences can only be 20 characters long on a 20x4 display!
        print("Writing to display")
        display.lcd_display_string("  Greetings Human! ", 1)  # Write line of text to first line of display
        display.lcd_display_string("  This is a 20x4   ", 2)  # Write line of text to second line of display
        display.lcd_display_string("  LCD Display!     ", 3)  # Write line of text to third line of display
        display.lcd_display_string("Demo Pi Guy code    ", 4)  # Write line of text to fourth line of display
        sleep(3)                                              # Give time for the message to be read
        display.lcd_display_string("I am a 20x4 display!", 1)  # Refresh the first line of display with a different message
        display.lcd_display_string("I have 4 lines and  ", 2)  # Second line
        display.lcd_display_string("20 characters/line! ", 3)  # Third line
        display.lcd_display_string("Isn't that awesome? ", 4)  # Fourth line
        sleep(3)                                              # Give time for the message to be read
        display.lcd_clear()                                   # Clear the display of any data
        sleep(2)                                              # Give time for the message to be read
except KeyboardInterrupt:
    # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup
    print("Cleaning up!")
    display.lcd_clear()
