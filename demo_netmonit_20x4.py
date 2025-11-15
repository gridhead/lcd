#!/usr/bin/env python

# Network Monitor for 20x4 LCD - Enhanced to show more info at once
# Based on the original by @cgomesu

import drivers
from time import sleep
from os import devnull
from subprocess import call, check_output


def cleanup():
    display.lcd_clear()


def end(msg=None, status=0):
    cleanup()
    display.lcd_display_string('{:^20}'.format('# Bye message: #'), 1)
    display.lcd_display_string('{:^20}'.format(msg), 2)
    exit(status)


# Returns True if host responds to a ping request within the timeout interval
def ping(host, timeout=3):
    return call(['ping', '-c', '1', '-W', str(timeout), str(host)],
                stdout=open(devnull, 'w'),
                stderr=open(devnull, 'w')) == 0


# Returns True if host has given port open
def nc(host, port, timeout=3):
    return call(['nc', '-z', '-w', str(timeout), str(host), str(port)], stderr=open(devnull, 'w')) == 0


# Takes advantage of 20x4 display to show more information
def lcd_print_20x4(line1=None, line2=None, line3=None, line4=None, delay=5):
    display.lcd_clear()
    if line1:
        display.lcd_display_string('{:^20}'.format(line1), 1)
    if line2:
        display.lcd_display_string('{:^20}'.format(line2), 2)
    if line3:
        display.lcd_display_string('{:^20}'.format(line3), 3)
    if line4:
        display.lcd_display_string('{:^20}'.format(line4), 4)
    sleep(delay)


# Show scrolling text for longer messages
def lcd_scroll(text='', line=1, num_cols=20, delay=0.5):
    if len(text) > num_cols:
        display.lcd_display_string(text[:num_cols], line)
        sleep(1)
        for i in range(len(text) - num_cols + 1):
            text_to_print = text[i:i+num_cols]
            display.lcd_display_string(text_to_print, line)
            sleep(delay)
        sleep(1)
    else:
        display.lcd_display_string('{:^20}'.format(text), line)


def main():
    try:
        lcd_print_20x4(line1="### Welcome to ###",
                       line2="## NetMonitor ##",
                       line3="  20x4 Edition  ",
                       line4="",
                       delay=5)

        # Get hostname and IP
        try:
            hostname = check_output(['hostname'], encoding='utf8').strip()
            ip_addr = check_output(['hostname', '-I'], encoding='utf8').split()[0]
        except:
            hostname = "Unknown"
            ip_addr = "Unknown"

        lcd_print_20x4(line1="# Who am I?? #",
                       line2="Host: " + hostname[:14],
                       line3="IP: " + ip_addr,
                       line4="",
                       delay=5)

        while True:
            # Check all hosts and services, show multiple at once
            display.lcd_clear()
            display.lcd_display_string("# NetMonitor #", 1)

            # Check hosts
            host_status = []
            for host, address in hosts.items():
                status = "UP" if ping(address) else "DOWN"
                host_status.append("{}: {}".format(host[:8], status))

            # Check services
            service_status = []
            for service, address in services.items():
                status = "UP" if nc(address['ip'], address['port']) else "DOWN"
                service_status.append("{}: {}".format(service[:8], status))

            # Display up to 3 items at once
            all_status = host_status + service_status
            for i in range(0, len(all_status), 3):
                display.lcd_clear()
                display.lcd_display_string('{:^20}'.format("# NetMonitor #"), 1)
                if i < len(all_status):
                    display.lcd_display_string(all_status[i][:20], 2)
                if i+1 < len(all_status):
                    display.lcd_display_string(all_status[i+1][:20], 3)
                if i+2 < len(all_status):
                    display.lcd_display_string(all_status[i+2][:20], 4)
                sleep(3)

    except KeyboardInterrupt:
        end('Signal to stop', 0)
    except (RuntimeError, IOError):
        end('I2C bus error', 1)


if __name__ == "__main__":
    # create a display object from the Lcd class for 20x4 LCD
    display = drivers.Lcd(cols=20, rows=4)
    # customizable dict of unique, pingable hosts
    hosts = {
        'Internet': '8.8.8.8',
        'Firewall': '192.168.1.1',
        'NAS': '192.168.1.2'
    }
    # customizable dict of unique, netcatable services
    services = {
        'Cameras': {'ip': '192.168.1.2', 'port': '8000'},
        'Plex': {'ip': '192.168.1.2', 'port': '32400'}
    }
    main()
