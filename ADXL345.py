import spidev
import time

class adxl345:

	
	def __init__(self):
		self.spi = spidev.SpiDev()
		self.spi.open(0,0)
		self.spi.mode = 3
		self.spi.max_speed_hz = 5000000
		
			
		#Defind register hex
		self.DEVID = 0x00
		self.BW_RATE = 0x2C #set output data rate
		self.DATA_FORMAT = 0x31 # select wire mode
		self.POWER_CTL = 0x2D #set measuring mode
		self.DATAX0 = 0x32
		self.FIFO_CTL = 0x38
		
		self.write_register(self.POWER_CTL, 0x08) # start measuring 
		self.write_register(self.BW_RATE, 0x0F) #set the sampling rate to max(3.2k hz)
		self.write_register(self.FIFO_CTL, 0x80) #enable fifo stream mode
		
	
	def write_register(self, register, value):
		#0x7F ensures 'write' mode
		self.spi.xfer2([register & 0x7F, value])
	

	
	def read_register(self, register):
		cmd = 0xC0 | register #0xC0 ensures read and multi-bytes sampling mode
		resp = self.spi.xfer2([cmd] + [0]*6) # send commend & register byte + 6 dummy bytes
		
		#returns bytes without the first(dummy) byte
		return resp[1:]
	
	def measure(self):
		fifo_status = read_register(0x39)  & 0x3F
		timestamp = time.time()
		response = self.read_register(self.DATAX0)
		#shift high byte to left and combine with low byte
		x = (response[1] << 8) | response[0]
		y = (response[3] << 8) | response[2]
		z = (response[5] << 8) | response[4]

		return {
			'timestamp': timestamp,
			'x': x,
			'y': y,
			'z': z,
			}




