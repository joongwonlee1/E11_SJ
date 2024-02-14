import sys
import random
import time
import csv

start_time = time.time()
run_time = 30
run_time = int(sys.argv[1])
now = start_time

filename = "test_data.csv"
filename = sys.argv[2]
file = open(filename, "w", newline='')
dwriter = csv.writer(file)

meta_data = ["Time", "Data"]
dwriter.writerow(meta_data)
print(meta_data)

while (now-start_time) < run_time:
    time.sleep(1)
    data = random.random()
    now = time.time()
    datalist = [now,data]
    dwriter.writerow(datalist)
    print(datalist)