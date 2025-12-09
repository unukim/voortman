from ADXL345 import adxl345
import time
from datetime import datetime
import csv
from Database import database

sensor = adxl345(int_pin =17)
db = database(
		host = "192.168.100.112",
		port = "5435",
		database = "postgres",
		user = "yunhukim",
		password = "Unu706903!",
		)
		
model_type = "old"
bearing_type = "A"
data =[]

first_sample = sensor.read_fifo()
start_time = first_sample['time']
start_time_date = datetime.fromtimestamp(start_time)
data.append(first_sample)

while True:
	sample = sensor.read_fifo()
	if sample:
		data.append(sample)
		now = time.time()
		sample["datetime"] = datetime.fromtimestamp(sample["time"]).strftime("%Y-%m-%d %H:%M:%S.%f")
		if now - start_time >= 1.0:
			break

duration = now - start_time
print(len(data), "data collected for", duration, "seconds")

start_timestamp = data[0]["time"]
for sample in data:
	sample['timestamp'] = sample['time'] - start_timestamp
	
#save to csv file
filename = f"{model_type}_{start_time_date}.csv"
with open(filename, mode ='w', newline='') as file:
	writer = csv.DictWriter(file, fieldnames = ["datetime", "timestamp","time", "x", "y", "z"])
	writer.writeheader()
	writer.writerows(data)


machine_id = db.insert_machine(model_type, bearing_type)
session_id = db.insert_session(
				machine_id = machine_id, 
				start_time = start_time_date, 
				duration = duration
				)

for sample in data:
	db.insert_raw_data(session_id, sample['timestamp'], sample)
