import RPi.GPIO as GPIO
import time
import pandas as pd

lst = []
channel = 17
last_time = time.time()
event_counter = 0
last_list_size = 0
increase_counter = 0
last_increase_time = time.time()

def my_callback(channel):
    global lst, event_counter  # Include event_counter as global
    current_time = time.time()  # Capture the current time once for consistency
    if GPIO.input(channel) == GPIO.LOW:
        print('\n▲ at ' + str(current_time))
        lst.append((current_time, "LOW"))
    else:
        print('\n▼ at ' + str(current_time))
        lst.append((current_time, "HIGH"))
    event_counter += 1  # Increment event_counter for both HIGH and LOW

try:
    runtime = int(input("Enter runtime in seconds: "))
    count_interval = int(input("Enter the counting interval: "))
    filename = input("Enter output filename (without extension): ")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(channel, GPIO.BOTH, callback=my_callback)

    input('\nPress Enter to start recording...\n')  # Corrected the escape sequence
    start_time = time.time()

    while (time.time() - start_time) < runtime:
        current_time = time.time()
        if current_time - last_time >= count_interval:
            lst.append((current_time, "Count Interval", event_counter))
            last_time = current_time  # Update last_time correctly
            event_counter = 0  # Reset event_counter after logging it
        
        if len(lst) > last_list_size:
            increase_counter += 1
            last_list_size = len(lst)
            
        if current_time - last_increase_time >= count_interval:
            print("increase counter")
            increase_counter = 0
            last_increase_time = current_time
            
        # Adjust the sleep time to avoid long waits or negative sleep
        time.sleep(max(0, count_interval - (current_time - start_time) % count_interval))
        
finally:
    GPIO.cleanup()  # Ensure GPIO resources are freed even if an error occurs

print("Writing data to CSV...")

# Corrected to include the correct column names
col_names = ["Time", "State", "Event Counter"]  # Update column names if you're including event counters directly in your list
df = pd.DataFrame(lst, columns=col_names)
df.to_csv(filename + ".csv", index=False)

print("Data written to", filename + ".csv")

