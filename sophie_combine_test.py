import adafruit_bme680
import time
import board
import pandas as pd
import busio
from digitalio import DigitalInOut, Direction, Pull
from adafruit_pm25.i2c import PM25_I2C
import serial
from adafruit_pm25.uart import PM25_UART

# Initialize I2C and UART
i2c = board.I2C()
uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=0.25)

# Initialize BME680 sensor
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)
bme680.sea_level_pressure = 1013.25

# Initialize PM2.5 sensor
reset_pin = None
pm25 = PM25_UART(uart, reset_pin)

# Create empty lists to store sensor data
weather_data = []
air_data = []

# Collect weather data
for i in range(10):
    sublst = []
    sublst.append(time.time())
    sublst.append("%0.1f" % bme680.temperature)
    sublst.append("%d" % bme680.gas)
    sublst.append("%0.1f" % bme680.relative_humidity)
    sublst.append("%0.3f" % bme680.pressure)
    sublst.append("%0.2f" % bme680.altitude)
    weather_data.append(sublst)
    time.sleep(1)

# Collect air quality data
for i in range(30):
    try:
        aqdata = pm25.read()
    except RuntimeError:
        print("Unable to read from sensor, retrying...")
        continue
    sublst = []
    sublst.append(time.time())
    sublst.append("%0.1f" % aqdata["particles 10um"])
    sublst.append("%d" % aqdata["particles 25um"])
    sublst.append("%0.1f" % aqdata["particles 100um"])
    air_data.append(sublst)
    time.sleep(1)

# Define column names for weather and air quality data
weather_col_names = ["Time", "Temperature", "Gas", "Humidity", "Pressure", "Altitude"]
air_col_names = ["Time", "pm10 standard", "pm25 standard", "pm100 env"]

# Create dataframes for weather and air quality data
weather_df = pd.DataFrame(weather_data, columns=weather_col_names)
air_df = pd.DataFrame(air_data, columns=air_col_names)

# Merge dataframes on 'Time' column
merged_df = pd.merge(weather_df, air_df, on="Time", how="outer")

# Output merged dataframe to a CSV file
merged_df.to_csv('weather_and_air_data.csv', index=False)
