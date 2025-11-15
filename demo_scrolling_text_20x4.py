#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Example: Scrolling text on 20x4 display if the string length is major than columns in display.
# Based on the original by Dídac García.

# Import necessary libraries for communication and display use
import drivers
from time import sleep

# Load the driver and set it to "display" for 20x4 LCD
# If you use something from the driver library use the "display." prefix first
display = drivers.Lcd(cols=20, rows=4)

# Main body of code
try:
	print("Press CTRL + C to stop this script!")

	def long_string(display, text='', num_line=1, num_cols=20):
		"""
		Parameters: (driver, string to print, number of line to print, number of columns of your display)
		Return: This function send to display your scrolling string.
		"""
		if len(text) > num_cols:
			display.lcd_display_string(text[:num_cols], num_line)
			sleep(1)
			for i in range(len(text) - num_cols + 1):
				text_to_print = text[i:i+num_cols]
				display.lcd_display_string(text_to_print, num_line)
				sleep(0.2)
			sleep(1)
		else:
			display.lcd_display_string(text, num_line)


	# Example of short string
	long_string(display, "Hello World!", 1)
	sleep(1)

	# Example of long string on line 2
	long_string(display, "Hello again. This is a long text for 20x4 display.", 2)

	# Display static text on other lines
	display.lcd_display_string("Line 3: Static text", 3)
	display.lcd_display_string("Line 4: More text", 4)
	sleep(2)

	display.lcd_clear()
	sleep(1)

	while True:
		# An example of infinite scrolling text on multiple lines
		display.lcd_display_string("20x4 Scrolling Demo", 1)
		long_string(display, "This is line 2 with a very long scrolling message!", 2)
		long_string(display, "Line 3 also scrolls if the text is too long to fit!", 3)
		display.lcd_display_string("Line 4: Static", 4)
except KeyboardInterrupt:
	# If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup
	print("Cleaning up!")
	display.lcd_clear()
