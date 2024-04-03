import time
import pandas as pd
import RPi.GPIO as GPIO
import sys

lst = []
runtime = int(sys.argv[1])
filename = sys.argv[2]
print("hello")
channel = 17

for i in range (runtime):
	print("hello2")
	sublst = []
	if GPIO.input(channel) == GPIO.LOW:
		print('\n ▲ at ' + str(time.time()))
		sublst.append(time.time())
		lst.append(sublst)
	else:
		print('\n▼  at ' + str(time.time()))

 
try:
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	PIO.add_event_detect(17, GPIO.BOTH, callback=my_callback)
 
	message = input('\nPress any key to exit.\n')
 
	finally:
		GPIO.cleanup()


#col_names = ["Time"]
#df = pd.DataFrame(lst, columns = col_names)
#csv_data = df.to_csv(filename, index = False)
