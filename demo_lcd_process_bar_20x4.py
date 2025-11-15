#! /usr/bin/env python

# Program showing animated progress bars using custom characters for 20x4 LCD.
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

# Redefine the default characters that will be used to create process bar:
# Left full character. Code {0x00}.
cc.char_1_data = ["01111",
                  "11000",
                  "10011",
                  "10111",
                  "10111",
                  "10011",
                  "11000",
                  "01111"]

# Left empty character. Code {0x01}.
cc.char_2_data = ["01111",
                  "11000",
                  "10000",
                  "10000",
                  "10000",
                  "10000",
                  "11000",
                  "01111"]

# Central full character. Code {0x02}.
cc.char_3_data = ["11111",
                  "00000",
                  "11011",
                  "11011",
                  "11011",
                  "11011",
                  "00000",
                  "11111"]

# Central empty character. Code {0x03}.
cc.char_4_data = ["11111",
                  "00000",
                  "00000",
                  "00000",
                  "00000",
                  "00000",
                  "00000",
                  "11111"]

# Right full character. Code {0x04}.
cc.char_5_data = ["11110",
                  "00011",
                  "11001",
                  "11101",
                  "11101",
                  "11001",
                  "00011",
                  "11110"]

# Right empty character. Code {0x05}.
cc.char_6_data = ["11110",
                  "00011",
                  "00001",
                  "00001",
                  "00001",
                  "00001",
                  "00011",
                  "11110"]

# Load custom characters data to CG RAM:
cc.load_custom_characters_data()

MIN_CHARGE = 0
MAX_CHARGE = 100

# Main body of code
charge = 0
charge_delta = 5
bar_repr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # 14 segments for 20 char width

try:
    while True:
        display.lcd_display_string("20x4 Progress Demo", 1)
        display.lcd_display_string("Battery Charge:", 2)

        # Render charge bar (using 14 characters for the bar)
        bar_string = ""
        for i in range(14):
            if i == 0:
                # Left character
                if bar_repr[i] == 0:
                    # Left empty character
                    bar_string = bar_string + "{0x01}"
                else:
                    # Left full character
                    bar_string = bar_string + "{0x00}"
            elif i == 13:
                # Right character
                if bar_repr[i] == 0:
                    # Right empty character
                    bar_string = bar_string + "{0x05}"
                else:
                    # Right full character
                    bar_string = bar_string + "{0x04}"
            else:
                # Central character
                if bar_repr[i] == 0:
                    # Central empty character
                    bar_string = bar_string + "{0x03}"
                else:
                    # Central full character
                    bar_string = bar_string + "{0x02}"

        # Print the string to display with percentage
        display.lcd_display_extended_string(bar_string + " {0}%".format(charge), 3)

        # Display charging status on line 4
        if charge_delta > 0:
            display.lcd_display_string("Status: Charging   ", 4)
        else:
            display.lcd_display_string("Status: Discharging", 4)

        # Update the charge and recalculate bar_repr
        charge += charge_delta
        if (charge >= MAX_CHARGE) or (charge <= MIN_CHARGE):
            charge_delta = -1 * charge_delta

        for i in range(14):
            segment_value = ((i + 1) * 100) // 14
            if charge >= segment_value:
                bar_repr[i] = 1
            else:
                bar_repr[i] = 0

        # Wait for some time
        sleep(1)

except KeyboardInterrupt:
    # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup
    print("Cleaning up!")
    display.lcd_clear()
