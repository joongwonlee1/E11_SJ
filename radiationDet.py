import RPi.GPIO as GPIO
import time
import pandas as pd

lst = []
channel = 17
def my_callback(channel):
    global lst
    if GPIO.input(channel) == GPIO.LOW:
        print('\n ▲ at ' + str(time.time()))
        lst.append((time.time(), "LOW"))
    else:
        print('\n▼  at ' + str(time.time()))
        lst.append((time.time(), "HIGH"))

try:
    runtime = int(input("Enter runtime in seconds: "))
    filename = input("Enter output filename (without extension): ")

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(17, GPIO.BOTH, callback=my_callback)

    input('\nPress Enter to start recording...\\n')
    start_time = time.time()

    while (time.time() - start_time) < runtime:
        pass  # Wait until runtime is reached

finally:
    GPIO.cleanup()

print("Writing data to CSV...")

col_names = ["Time", "State"]
df = pd.DataFrame(lst, columns=col_names)
df.to_csv(filename + ".csv", index=False)

print("Data written to", filename + ".csv")
