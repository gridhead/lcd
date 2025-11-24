#! /usr/bin/env python

# Weather information display for 20x4 LCD with rotating pages
# Uses WeatherAPI.com for weather data
# Demo program for the I2C 20x4 Display

import drivers
import requests
import os
from time import sleep
from datetime import datetime

# Configuration
API_KEY = os.getenv("WEATHER_API_KEY")  # Set via environment variable
LOCATION = os.getenv("WEATHER_LOCATION", "London")  # Set via environment variable, defaults to London
UPDATE_INTERVAL = 300  # Update weather data every 5 minutes (300 seconds)

# Load the driver and set it to "display" for 20x4 LCD
display = drivers.Lcd(cols=20, rows=4)

def get_weather_data():
    """
    Fetch weather data from WeatherAPI.com
    Returns a dictionary with weather information or None if error
    """
    try:
        # WeatherAPI.com endpoint with current weather and AQI
        url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={LOCATION}&aqi=yes"

        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Extract relevant data
        current = data['current']

        weather_data = {
            'temp': int(current['temp_c']),
            'feels_like': int(current['feelslike_c']),
            'humidity': current['humidity'],
            'aqi': int(current.get('air_quality', {}).get('pm2_5', 0)),  # PM2.5 in µg/m³
            'pressure': int(current['pressure_mb']),
            'condition': current['condition']['text'],
            'wind_speed': int(current['wind_kph']),
        }

        # Get forecast for tomorrow's temps
        forecast_url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={LOCATION}&days=2"
        forecast_response = requests.get(forecast_url, timeout=10)
        forecast_response.raise_for_status()
        forecast_data = forecast_response.json()

        tomorrow = forecast_data['forecast']['forecastday'][1]['day']
        weather_data['temp_min'] = int(tomorrow['mintemp_c'])
        weather_data['temp_max'] = int(tomorrow['maxtemp_c'])
        weather_data['rain_prob'] = int(tomorrow['daily_chance_of_rain'])

        return weather_data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None
    except (KeyError, IndexError) as e:
        print(f"Error parsing weather data: {e}")
        return None

def display_page_1(data, now):
    """Display first page: current conditions"""
    # Line 1: Temperature and Humidity
    line1 = f"Tmp:{data['temp']:>3}\xDFC  Hum:{data['humidity']:>3}%"

    # Line 2: AQI (PM2.5) and Pressure
    line2 = f"AQI:{data['aqi']:<4} Prs:{data['pressure']}mb"

    # Line 3: Condition and Wind
    condition = data['condition'][:9]  # Limit to 9 chars
    line3 = f"{condition:<9} Wnd:{data['wind_speed']:>2}km"

    # Line 4: Time and Date
    time_str = now.strftime("%I:%M%p")
    date_str = now.strftime("%a %d")
    line4 = f"{time_str:<8} {date_str:>11}"

    display.lcd_display_string(line1, 1)
    display.lcd_display_string(line2, 2)
    display.lcd_display_string(line3, 3)
    display.lcd_display_string(line4, 4)

def display_page_2(data):
    """Display second page: detailed forecast"""
    # Line 1: Current temp and feels like
    line1 = f"Tmp:{data['temp']:>3}\xDFC  Fls:{data['feels_like']:>3}\xDFC"

    # Line 2: Humidity and AQI
    line2 = f"Hum:{data['humidity']:>3}%  AQI:{data['aqi']:<4}"

    # Line 3: Condition and Rain probability
    condition = data['condition'][:10]  # Limit to 10 chars
    line3 = f"{condition:<10} Rn:{data['rain_prob']:>2}%"

    # Line 4: Tomorrow's temperature range
    line4 = f"Tmr:{data['temp_min']:>3}-{data['temp_max']:>2}\xDFC"

    display.lcd_display_string(line1, 1)
    display.lcd_display_string(line2, 2)
    display.lcd_display_string(line3, 3)
    display.lcd_display_string(line4, 4)

def display_error(message):
    """Display error message on LCD"""
    display.lcd_clear()
    display.lcd_display_string("    Weather Error   ", 1)
    display.lcd_display_string("====================", 2)
    display.lcd_display_string(message[:20].center(20), 3)
    display.lcd_display_string("Retrying...         ", 4)

# Main program
try:
    # Check if API key is set
    if not API_KEY:
        print("ERROR: WEATHER_API_KEY environment variable not set!")
        print("Set it with: export WEATHER_API_KEY='your_api_key_here'")
        display.lcd_display_string("  ERROR: No API Key ", 1)
        display.lcd_display_string("Set WEATHER_API_KEY  ", 2)
        display.lcd_display_string("environment variable ", 3)
        exit(1)

    print("Starting weather display...")
    print(f"Location: {LOCATION}")

    # Initial display
    display.lcd_display_string("  Weather Display   ", 1)
    display.lcd_display_string("====================", 2)
    display.lcd_display_string("  Loading data...   ", 3)
    display.lcd_display_string("                    ", 4)

    page = 1
    cycle_counter = 0
    weather = None
    last_update = 0

    while True:
        current_time = datetime.now()
        time_elapsed = (current_time.timestamp() - last_update)

        # Fetch weather data on first run or after UPDATE_INTERVAL
        if weather is None or time_elapsed >= UPDATE_INTERVAL:
            print("Fetching weather data...")
            weather = get_weather_data()
            last_update = current_time.timestamp()

            if weather is None:
                display_error("Check API key/net")
                sleep(10)
                continue
            else:
                print("Weather data updated successfully")

        # Display current page
        if page == 1:
            display_page_1(weather, current_time)
        else:
            display_page_2(weather)

        sleep(10)

        # Switch pages every 10 seconds
        page = 2 if page == 1 else 1
        cycle_counter += 1

except KeyboardInterrupt:
    # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup
    print("\nCleaning up!")
    display.lcd_clear()
