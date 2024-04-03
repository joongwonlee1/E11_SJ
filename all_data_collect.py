import adafruit_bme680
import time
import board
import pandas as pd
from digitalio import DigitalInOut, Direction, Pull
from adafruit_pm25.i2c import PM25_I2C
import serial
import RPi.GPIO as GPIO

def collect_data():
    # Collect BME680 weather data
    i2c = board.I2C()
    bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)
    bme680.sea_level_pressure = 1013.25
    weather_data = []
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
    
    # Collect PM2.5 air quality data
    reset_pin = None
    uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=0.25)
    pm25 = PM25_I2C(uart, reset_pin)
    air_data = []
    for i in range(30):
        try:
            aqdata = pm25.read()
        except RuntimeError:
            print("Unable to read from sensor, retrying...")
            continue
        sublst = []
        sublst.append(time.time())
        sublst.append("%0.1f" % aqdata["particles 10um"])
        sublst.append("%0.1f" % aqdata["particles 25um"])
        sublst.append("%0.1f" % aqdata["particles 100um"])
        air_data.append(sublst)
        time.sleep(1)
    
    # Collect GPIO data
    lst = []
    channel = 17
    event_counter = 0

    def my_callback(channel):
        if GPIO.input(channel) == GPIO.LOW:
            lst.append((time.time(), "LOW"))
        else:
            lst.append((time.time(), "HIGH"))
            event_counter +=1

    runtime = int(input("Enter runtime in seconds: "))
    count_interval = int(input("Enter the counting interval: "))
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(17, GPIO.BOTH, callback=my_callback)

    input('\nPress Enter to start recording...\\n')
    start_time = time.time()

    while (time.time() - start_time) < runtime:
        if time.time() - start_time >= count_interval:
            lst.append(("Count Interval", event_counter))
            start_time = time.time()

        time.sleep(1)

    GPIO.cleanup()
    
    # Write data to CSV
    ##new
    col_names = ["Time", "State"]
    df_gpio = pd.DataFrame(lst, columns=col_names)
    df_gpio.to_csv('rad_data_new.csv', index=False)
    
    col_names_weather = ["Time","Temperature", "Gas","Humidity", "Pressure", "Altitude"]
    df_weather = pd.DataFrame(weather_data, columns=col_names_weather)
    df_weather.to_csv('weather_data_new.csv', index=False)
    
    col_names_air = ["Time","pm10 standard", "pm25 standard","pm100 env"]
    df_air = pd.DataFrame(air_data, columns=col_names_air)
    df_air.to_csv('air_data_new.csv', index=False)
    
    print("Data written to rad_data_new.csv, weather_data_new.csv, and air_data_new.csv")

# Call the function to collect all data
collect_data()
