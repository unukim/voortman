from ADXL345 import adxl345
import time
from datetime import datetime

sensor = adxl345(int_pin =17)
data =[]

first_sample = sensor.read_fifo()
start_time = first_sample['timestamp']
data.append(first_sample)

while True:
	sample = sensor.read_fifo()
	if sample:
		data.append(sample)
		elasped = (sample['timestamp'] - start_time).total_seconds()
		if elasped >= 1.0:
			break

print(data[0:15])
print(data[-1])
print(len(data))
