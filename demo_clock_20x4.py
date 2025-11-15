#! /usr/bin/env python

# Simple clock program for 20x4 LCD. Writes date and time.
# Demo program for the I2C 20x4 Display
# Based on the original by Matthew Timmons-Brown for The Raspberry Pi Guy YouTube channel

# Import necessary libraries for communication and display use
import drivers
from time import sleep
from datetime import datetime

# Load the driver and set it to "display" for 20x4 LCD
# If you use something from the driver library use the "display." prefix first
display = drivers.Lcd(cols=20, rows=4)

try:
    print("Writing to display")
    display.lcd_display_string("  20x4 LCD Clock", 1)  # Write line of text to first line of display
    display.lcd_display_string("====================", 2)  # Separator line
    while True:
        # Write the date and time to the display
        now = datetime.now()
        display.lcd_display_string("Date: " + now.strftime("%Y-%m-%d"), 3)
        display.lcd_display_string("Time: " + now.strftime("%H:%M:%S"), 4)
        sleep(1)  # Update every second
except KeyboardInterrupt:
    # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup
    print("Cleaning up!")
    display.lcd_clear()
