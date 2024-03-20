import RPi.GPIO as GPIO
import time
import pandas as pd

# List to store event data
lst = []

# GPIO setup
channel = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Variables for tracking
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

    input('\nPress Enter to start recording...\n')
    start_time = time.time()

    while (time.time() - start_time) < runtime:
        current_time = time.time()
        if current_time - last_interval_time >= count_interval:
            # Log the interval metadata
            lst.append((last_interval_time, interval_number, event_counter))
            last_interval_time = current_time
            event_counter = 0  # Reset the event counter for the next interval
            interval_number += 1  # Increment the interval number
        
        # Sleep for the remainder of the current interval to reduce CPU usage
        sleep_time = count_interval - (current_time - last_interval_time)
        if sleep_time > 0:
            time.sleep(sleep_time)

finally:
    GPIO.cleanup()  # Clean up GPIO

# Writing data to CSV
print("Writing data to CSV...")
col_names = ["Interval Start Time", "Interval Number", "Event Count"]
df = pd.DataFrame(lst, columns=col_names)

# Formatting the "Interval Start Time" to a readable format
df['Interval Start Time'] = pd.to_datetime(df['Interval Start Time'], unit='s')
df.to_csv(filename + ".csv", index=False)
print("Data written to", filename + ".csv")

