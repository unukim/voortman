import spidev
import time
from datetime import datetime

class adxl345:

	
	def __init__(self):
		self.spi = spidev.SpiDev()
		self.spi.open(0,0)
		self.spi.mode = 3
		self.spi.max_speed_hz = 5000000
		self.sample_rate = 3200
		self.dt = 1.0 / self.sample_rate
		
			
		#Defind register hex
		self.DEVID = 0x00
		self.BW_RATE = 0x2C #set output data rate
		self.DATA_FORMAT = 0x31 # select wire mode
		self.POWER_CTL = 0x2D #set measuring mode
		self.DATAX0 = 0x32
		self.FIFO_CTL = 0x38
		self.FIFO_STATUS =0x39
		
		self.write_register(self.POWER_CTL, 0x08) # start measuring 
		self.write_register(self.BW_RATE, 0x0F) #set the sampling rate to max(3.2k hz)
		self.write_register(self.FIFO_CTL, 0x80) #enable fifo stream mode
		self.write_register(self.DATA_FORMAT, 0x08) #full resolution mode
		
	
	def write_register(self, register, value):
		#0x7F ensures 'write' mode
		self.spi.xfer2([register & 0x7F, value])
	

	
	def read_register_single(self, register):
		cmd = 0x80 | register #0x80 ensures read and single byte sampling mode
		resp = self.spi.xfer2([cmd] + [0]*6) # send commend & register byte + 6 dummy bytes
		
		return resp[1]
		
	def read_register_multi(self, register, length):
		cmd = 0xC0 | register #0xC0 ensures read and multi-byte sampling mode
		resp = self.spi.xfer2([cmd] + [0x00]*length) # send commend & register byte + 6 dummy bytes
		
		#returns bytes without the first(dummy) byte
		return resp[1:]
	def to_signed(self,val):
		if val & 0x8000:
			return val - 65536
		return val

	def measure(self):
		fifo_status = self.read_register_single(self.FIFO_STATUS) & 0x3F
		timestamp = time.time()
		data = self.read_register_multi(self.DATAX0,6)
		#shift high byte to left and combine with low byte
		x = self.to_signed(data[1] << 8 | data[0]) *0.0039
		y = self.to_signed(data[3] << 8 | data[2]) *0.0039
		z = self.to_signed(data[5] << 8 | data[4]) *0.0039
		
		time.sleep(self.dt)
		return {
			'timestamp': timestamp,
			'x': x,
			'y': y,
			'z': z,
			}




