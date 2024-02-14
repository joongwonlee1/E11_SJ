import adafruit_bme680
import time
import board
import pandas as pd
import busio
from digitalio import DigitalInOut, Direction, Pull
from adafruit_pm25.i2c import PM25_I2C


reset_pin = None
import serial
uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=0.25)
from adafruit_pm25.uart import PM25_UART
pm25 = PM25_UART(uart, reset_pin)

print("Found PM2.5 sensor, reading data...")

i2c= board.I2C()
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)

bme680.sea_level_pressure = 1013.25
#start = time.time()
lst = []

for i in range(10):
    try:
        aqdata = pm25.read()
    except RuntimeError:
        print("Unable to read from sensor, retrying...")
        continue
    sublst = []
    sublst.append(time.time())
    sublst.append("%0.1f" % bme680.temperature)
    sublst.append("%d" % bme680.gas)
    sublst.append("%0.1f" % bme680.relative_humidity)
    sublst.append("%0.3f" % bme680.pressure)
    sublst.append("%0.2f" %bme680.altitude)
    sublst.append("%0.1f" % aqdata["particles 10um"])
    sublst.append("%d" % aqdata["particles 25um"])
    sublst.append("%0.1f" % aqdata["particles 100um"])
    lst.append(sublst)
    time.sleep(1)


col_names = ["Time","Temperature", "Gas","Humidity", "Pressure", "Altitude","pm10 standard", "pm25 standard","pm100 env"]
df = pd.DataFrame(lst, columns = col_names)
csv_data = df.to_csv('combined_data.csv', index = False)