from ADXL345 import adxl345
import time
from datetime import datetime
import csv

sensor = adxl345(int_pin =17)
model = "old"
data =[]

first_sample = sensor.read_fifo()
start_time = first_sample['timestamp']
start_time_date = datetime.fromtimestamp(start_time)
data.append(first_sample)

while True:
	sample = sensor.read_fifo()
	if sample:
		data.append(sample)
		now = time.time()
		sample["datetime"] = datetime.fromtimestamp(sample["timestamp"]).strftime("%Y-%m-%d %H:%M:%S.%f")
		if now - start_time >= 1.0:
			break
print(len(data), "data collected for", now - start_time, "seconds")

#save to csv file
filename = f"{model}_{start_time_date}.csv"
with open(filename, mode ='w', newline='') as file:
	writer = csv.DictWriter(file, fieldnames = ["datetime", "timestamp", "x", "y", "z"])
	writer.writeheader()
	writer.writerows(data)


