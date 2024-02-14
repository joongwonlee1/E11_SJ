import time
import board
import busio
import pandas as pd
import adafruit_pm25
import adafruit_bme680

# Initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize PM2.5 sensor
reset_pin = None  
uart = busio.UART(board.TX, board.RX, baudrate=9600)
pm25 = adafruit_pm25.uart.PM25_UART(uart, reset_pin)

# Initialize BME680 sensor
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)
bme680.sea_level_pressure = 1013.25

# Data collection
pm25_data = []
bme680_data = []

for i in range(10):  # Adjust the number of iterations as needed
    try:
        # Read PM2.5 sensor data
        pm25_data.append([time.time(), "%0.1f" % pm25.read()["particles 10um"], "%0.1f" % pm25.read()["particles 25um"], "%0.1f" % pm25.read()["particles 100um"]])

        # Read BME680 sensor data
        bme680_data.append([time.time(), "%0.1f" % bme680.temperature, "%d" % bme680.gas, "%0.1f" % bme680.relative_humidity, "%0.3f" % bme680.pressure, "%0.2f" % bme680.altitude])
        
    except RuntimeError:
        print("Error reading sensor data")

    time.sleep(1)

# Convert collected data to DataFrames
pm25_col_names = ["Time", "pm10 standard", "pm25 standard", "pm100 env"]
pm25_df = pd.DataFrame(pm25_data, columns=pm25_col_names)

bme680_col_names = ["Time", "Temperature", "Gas", "Humidity", "Pressure", "Altitude"]
bme680_df = pd.DataFrame(bme680_data, columns=bme680_col_names)

# Save data to CSV files
pm25_csv_data = pm25_df.to_csv('pm25_data.csv', index=False)
bme680_csv_data = bme680_df.to_csv('bme680_data.csv', index=False)
