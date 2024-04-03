import adafruit_bme680
import time
import board
import pandas as pd

i2c= board.I2C()
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)

bme680.sea_level_pressure = 1013.25
#start = time.time()
lst = []

for i in range(10):
	sublst = []
	sublst.append(time.time())
	sublst.append("%0.1f" % bme680.temperature)
	sublst.append("%d" % bme680.gas)
	sublst.append("%0.1f" % bme680.relative_humidity)
	sublst.append("%0.3f" % bme680.pressure)
	sublst.append("%0.2f" %bme680.altitude)
	lst.append(sublst)
	time.sleep(1)


col_names = ["Time","Temperature", "Gas","Humidity", "Pressure", "Altitude"]
df = pd.DataFrame(lst, columns = col_names)
csv_data = df.to_csv('weather_data_collect.csv', index = False)

# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
Example sketch to connect to PM2.5 sensor with either I2C or UART.
"""

# pylint: disable=unused-import
import time
import board
import busio
from digitalio import DigitalInOut, Direction, Pull
from adafruit_pm25.i2c import PM25_I2C
import pandas as pd


reset_pin = None
# If you have a GPIO, its not a bad idea to connect it to the RESET pin
# reset_pin = DigitalInOut(board.G0)
# reset_pin.direction = Direction.OUTPUT
# reset_pin.value = False


# For use with a computer running Windows:
# import serial
# uart = serial.Serial("COM30", baudrate=9600, timeout=1)

# For use with microcontroller board:
# (Connect the sensor TX pin to the board/computer RX pin)
# uart = busio.UART(board.TX, board.RX, baudrate=9600)

# For use with Raspberry Pi/Linux:
import serial
uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=0.25)

# For use with USB-to-serial cable:
# import serial
# uart = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=0.25)

# Connect to a PM2.5 sensor over UART
from adafruit_pm25.uart import PM25_UART
pm25 = PM25_UART(uart, reset_pin)

# Create library object, use 'slow' 100KHz frequency!
# i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
# Connect to a PM2.5 sensor over I2C
# pm25 = PM25_I2C(i2c, reset_pin)

print("Found PM2.5 sensor, reading data...")

# while True:
    

    # print()
    # print("Concentration Units (standard)")
    # print("---------------------------------------")
    # print(
    #     "PM 1.0: %d\tPM2.5: %d\tPM10: %d"
    #     % (aqdata["pm10 standard"], aqdata["pm25 standard"], aqdata["pm100 standard"])
    # )
    # print("Concentration Units (environmental)")
    # print("---------------------------------------")
    # print(
    #     "PM 1.0: %d\tPM2.5: %d\tPM10: %d"
    #     % (aqdata["pm10 env"], aqdata["pm25 env"], aqdata["pm100 env"])
    # )
    # print("---------------------------------------")
    # print("Particles > 0.3um / 0.1L air:", aqdata["particles 03um"])
    # print("Particles > 0.5um / 0.1L air:", aqdata["particles 05um"])
    # print("Particles > 1.0um / 0.1L air:", aqdata["particles 10um"])
    # print("Particles > 2.5um / 0.1L air:", aqdata["particles 25um"])
    # print("Particles > 5.0um / 0.1L air:", aqdata["particles 50um"])
    # print("Particles > 10 um / 0.1L air:", aqdata["particles 100um"])
    # print("---------------------------------------")


lst = []

for i in range(30):
    try:
        aqdata = pm25.read()
        # print(aqdata)
    except RuntimeError:
        print("Unable to read from sensor, retrying...")
        continue
    sublst = []
    sublst.append(time.time())
    sublst.append("%0.1f" % aqdata["particles 10um"])
    sublst.append("%0.1f" % aqdata["particles 25um"])
    sublst.append("%0.1f" % aqdata["particles 100um"])
    lst.append(sublst)
    time.sleep(1)


col_names = ["Time","pm10 standard", "pm25 standard","pm100 env"]
df = pd.DataFrame(lst, columns = col_names)
csv_data = df.to_csv('air_data_collect.csv', index = False)

import RPi.GPIO as GPIO
import time
import pandas as pd

lst = []

channel = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

last_interval_time = time.time()
event_counter = 0
interval_number = 0

def my_callback(channel):
    global event_counter
    if GPIO.input(channel) == GPIO.LOW:
        print('\n▲ LOW at ' + str(time.time()))
    else:
        print('\n▼ HIGH at ' + str(time.time()))
    event_counter += 1

try:
    runtime = int(input("Enter runtime in seconds: "))
    count_interval = int(input("Enter the counting interval: "))
    filename = input("Enter output filename (without extension): ")
    
    GPIO.add_event_detect(channel, GPIO.BOTH, callback=my_callback)

    start_time = time.time()

    while (time.time() - start_time) < runtime + count_interval: 
        current_time = time.time()
        if current_time - last_interval_time >= count_interval:
            lst.append((last_interval_time, interval_number, event_counter))
            last_interval_time = current_time
            event_counter = 0  
            interval_number += 1  
        
        sleep_time = count_interval - (current_time - last_interval_time)
        if sleep_time > 0:
            time.sleep(sleep_time)

finally:
    GPIO.cleanup() 

if lst:
    lst.pop(0)
    
tup_new = (lst[0][0]-2,0,0)
lst.insert(0, tup_new)

# Writing data to CSV
print("Writing data to CSV...")
col_names = ["Interval Start Time", "Interval Number", "Event Count"]
df = pd.DataFrame(lst, columns=col_names)

df.to_csv(filename + ".csv", index=False)
print("Data written to", filename + ".csv")