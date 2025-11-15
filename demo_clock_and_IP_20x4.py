#! /usr/bin/env python

# Clock and IP address display for 20x4 LCD
# Demo program for the I2C 20x4 Display

import drivers
from time import sleep
from datetime import datetime
from subprocess import check_output

# Load the driver for 20x4 LCD
display = drivers.Lcd(cols=20, rows=4)

# Get IP address
try:
    IP = check_output(["hostname", "-I"], encoding="utf8").split()[0]
except:
    IP = "No network"

try:
    print("Writing to display")
    display.lcd_display_string("System Information", 1)
    display.lcd_display_string("--------------------", 2)
    while True:
        now = datetime.now()
        display.lcd_display_string("Time: " + now.strftime("%H:%M:%S"), 3)
        display.lcd_display_string("IP: " + IP, 4)
        sleep(1)
except KeyboardInterrupt:
    # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup
    print("Cleaning up!")
    display.lcd_clear()
