#!/usr/bin/python3
# ---------------------------------------------------------- 
# ms5607.py
# 
# Sample program to read the pressure of a MS5607 pressure
# sensor over I2C bus. 24.07.2014 - wyss@superspider.net
# Program must be executed as root user 'sudo ./ms5607.py'
# 
# Used quick2wire API because I2C transfer is non-Standard
# (read 3 bytes after device address without command byte)
# ----------------------------------------------------------

import quick2wire.i2c as i2c
import time
import numpy as np

# device address
DEVICE1 = 0x76
DEVICE2 = 0x77

# commands/registers
RESET 			= 0x1E

# D1 = Pressure Sensor
CONV_D1_256 	= 0x40
CONV_D1_512 	= 0x42
CONV_D1_1024 	= 0x44
CONV_D1_2048 	= 0x46
CONV_D1_4096 	= 0x48

# D2 = Temperature Sensor
CONV_D2_256 	= 0x50
CONV_D2_512 	= 0x52
CONV_D2_1024	= 0x54
CONV_D2_2048	= 0x56
CONV_D2_4096	= 0x58

ADC_READ		= 0x00
PROM_READ		= 0xA0 	# + (address << 1) 

P_data = [.0,.0,.0,.0,.0,.0,.0,.0]

def sendCmd(cmd):
	bus.transaction(i2c.writing_bytes(DEVICE1, cmd))

def read2ByteVal():
	byte1,byte2 = bus.transaction(i2c.reading(DEVICE1,2))[0]
	val = (byte1<<8)+byte2
	return val

def read3ByteVal():
	byte1,byte2,byte3 = bus.transaction(i2c.reading(DEVICE1,3))[0]
	val = (byte1<<16)+(byte2<<8)+(byte3)
	return val

with i2c.I2CMaster(1) as bus:  
	sendCmd(RESET)
	time.sleep(.003)

	# read PROM values
	sendCmd(PROM_READ+(1<<1))
	C1 = read2ByteVal()
	print("C1: %d" % C1)
	
	sendCmd(PROM_READ+(2<<1))
	C2 = read2ByteVal()
	print("C2: %d" % C2)
	
	sendCmd(PROM_READ+(3<<1))
	C3 = read2ByteVal()
	print("C3: %d" % C3)
	
	sendCmd(PROM_READ+(4<<1))
	C4 = read2ByteVal()
	print("C4: %d" % C4)
	
	sendCmd(PROM_READ+(5<<1))
	C5 = read2ByteVal()
	print("C5: %d" % C5)
	
	sendCmd(PROM_READ+(6<<1))
	C6 = read2ByteVal()
	print("C6: %d" % C6)
	
	while True:
		# read pressure and temperature
		sendCmd(CONV_D1_256)
		sendCmd(ADC_READ)
		time.sleep(.01)
		D1 = read3ByteVal()
		# print("D1: %d" % D1)
		
		sendCmd(CONV_D2_256)
		sendCmd(ADC_READ)
		time.sleep(.01)
		D2 = read3ByteVal()
		# print("D2: %d" % D2)
		
		# calculate temperature
		dT = D2-C5*(2**8)
		# print("dT (Difference T_act and T_ref): %d" % dT)
		
		TEMP = (2000+dT*C6/(2**23))/100.0
		# print("TEMP: %d" % TEMP)
		
		OFF = C2*(2**17)+(C4*dT)/(2**6)
		# print("OFF: %d" % OFF)
		
		SENS = C1*(2**16)+(C3*dT)/(2**7)
		# print("SENS: %d" % SENS)
		
		P = (D1*SENS/(2**21)-OFF)/(2**15)/100.0
		# print("P: %d" % P)
		
		# Mittelwert der Sensordaten
		P_data = np.roll(P_data,1)
		P_data[0] = P
		# print(P_data)
		P_mean = np.mean(P_data)
		
		print("Temperatur: %.2f °C" % TEMP)
		print("Luftdruck: %.2f mBar" % P_mean)
		
		time.sleep(1)
	
