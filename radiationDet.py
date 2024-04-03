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
