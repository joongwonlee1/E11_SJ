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
csv_data = df.to_csv('weather_data.csv', index = False)

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
csv_data = df.to_csv('air_data.csv', index = False)

import RPi.GPIO as GPIO
import time
import pandas as pd

lst = []
channel = 17
last_time = time.time()
event_counter = 0
last_list_size =0
increase_counter =0
last_increase_time = time.time()

def my_callback(channel):
    global lst
    if GPIO.input(channel) == GPIO.LOW:
        print('\n ▲ at ' + str(time.time()))
        lst.append((time.time(), "LOW"))
    else:
        print('\n▼  at ' + str(time.time()))
        lst.append((time.time(), "HIGH"))
        event_counter +=1

try:
    runtime = int(input("Enter runtime in seconds: "))
    count_interval = int(input("Enter the counting interval: "))
    filename = input("Enter output filename (without extension): ")
    event_counter = 0
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(17, GPIO.BOTH, callback=my_callback)

    input('\nPress Enter to start recording...\\n')
    start_time = time.time()

    while (time.time() - start_time) < runtime:
        if time.time() - last_time >= count_interval:
            lst.append(("Count Interval", event_counter))
            last_rest_time = time.time()
        
        if len(lst) > last_list_size:
            increase_counter +=1
            last_list_size = len(lst)
            
        if time.time() - last_increase_time >= count_interval:
            print("increase counter")
            increase_counter =0
            last_increase_time = time.time()
            
        time.sleep(runtime - (time.time() - start_time()))
            
        
        pass  # Wait until runtime is reached

finally:
    GPIO.cleanup()

print("Writing data to CSV...")

col_names = ["Time", "State"]
df = pd.DataFrame(lst, columns=col_names)
df.to_csv(filename + ".csv", index=False)


print("Data written to", filename + ".csv")