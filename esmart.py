# Library for communicating with eSmart 3 MPPT charger
# skagmo.com, 2018

import struct, time, serial, socket, requests
#from collections import namedtuple

# States
STATE_START = 0
STATE_DATA = 1

REQUEST_MSG0 = "\xaa\x01\x01\x01\x00\x03\x00\x00\x1e\x32"
LOAD_OFF = "\xaa\x01\x01\x02\x04\x04\x01\x00\xfe\x13\x38"
LOAD_ON = "\xaa\x01\x01\x02\x04\x04\x01\x00\xfd\x13\x39"

DEVICE_MODE = ["IDLE", "CC", "", "FLOAT", "STARTING"]

class esmart:
	def __init__(self):
		self.state = STATE_START
		self.data = ""
		self.callback = False
		self.port = ""
		self.timeout = 0

	def __del__(self):
		self.close()

	def set_callback(self, function):
		self.callback = function

	def open(self, port):
		self.ser = serial.Serial(port,9600,timeout=0.1)
		self.port = port

	def close(self):
		try:
			self.ser.close()
			self.ser = False
		except AttributeError:
			pass

	def send(self, pl):
		self.ser.write(self.pack(pl))

	def parse(self, data):
		for c in data:
			if (self.state == STATE_START):
				if (c == '\xaa'):
					# Start character detected
					self.state = STATE_DATA
					self.data = ""
					self.target_len = 255
				else:
					print c

			elif (self.state == STATE_DATA):
				self.data += c
				# Received enough of the packet to determine length
				if (len(self.data) == 5):
					self.target_len = 6 + ord(self.data[4])

				# Received whole packet
				if (len(self.data) == self.target_len):
					self.state = STATE_START

					#print " ".join("{:02x}".format(ord(c)) for c in self.data)

					# Source 3 is MPPT device
					if (ord(self.data[2]) == 3):
						msg_type = ord(self.data[3])

						# Type 0 packet contains most data
						if (ord(self.data[3]) == 0):
							fields['chg_mode'] = struct.unpack("<H", self.data[7:9])[0]
							fields['pv_volt'] = struct.unpack("<H", self.data[9:11])[0] / 10.0
							fields['bat_volt'] = struct.unpack("<H", self.data[11:13])[0] / 10.0
							fields['chg_cur'] = struct.unpack("<H", self.data[13:15])[0] / 10.0
							fields['load_volt'] = struct.unpack("<H", self.data[17:19])[0] / 10.0
							fields['load_cur'] = struct.unpack("<H", self.data[19:21])[0] / 10.0
							fields['chg_power'] = struct.unpack("<H", self.data[21:23])[0]
							fields['load_power'] = struct.unpack("<H", self.data[23:25])[0]
							fields['bat_temp'] = ord(self.data[25])
							fields['int_temp'] = ord(self.data[27])
							fields['soc'] = ord(self.data[29])
							fields['co2_gram'] = struct.unpack("<H", self.data[33:35])[0]

							self.callback(fields)

	def tick(self):
		try:
			while (self.ser.inWaiting()):
				self.parse(self.ser.read(100))

			# Send poll packet to request data every 5 seconds
			if (time.time() - self.timeout) > 5:
				self.ser.write(REQUEST_MSG0)
				self.timeout = time.time()
				#time.sleep(0.5)
				#self.ser.write(LOAD_OFF)

		except IOError:
			print("Serial port error, fixing")
			self.ser.close()
			opened = 0
			while not opened:
				try:
					self.ser = serial.Serial(self.port,38400,timeout=0)
					time.sleep(0.5)
					if self.ser.read(100):
						opened = 1	
					else:
						self.ser.close()		
				except serial.serialutil.SerialException:
					time.sleep(0.5)
					self.ser.close()
			print("Error fixed")

