#!/usr/bin/python
# ---------------------------------------------------------- 
# ms5607.py
# 
# Sample program to read the pressure of a MS5607 pressure
# sensor over I2C bus. 24.07.2014 - wyss@superspider.net
# Program must be executed as root user 'sudo ./ms5607.py'
# ----------------------------------------------------------

import smbus
import time

#bus = smbus.SMBus(0) # Rev 1 Pi uses bus 0
bus = smbus.SMBus(1)  # Rev 2 Pi uses bus 1

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

# reset sensor
bus.write_byte(DEVICE1,RESET)
time.sleep(0.003)

bus.write_byte(DEVICE1,CONV_D1_512)
bus.write_byte(DEVICE1,ADC_READ)

val = bus.read_word_data(DEVICE1,0)
#pressure = [0,0,0]
#pressure = bus.read_i2c_block_data(DEVICE1,0)

print val[0]
print val[1]
print val[2]

# this call only needed once at very first start and the delay should be in higher level
# b.write_quick(0x27)
# time.sleep(0.050)    # allow time for the conversion
# normally would expect an array defined at higher level
# val = [0,0,0,0]
# tell python which array to store results into and give correct number of parameters
# val = b.read_i2c_block_data( 0X27, 0 )
# X1 = (val[0] << 8) + val[1]
# Y1 = (val[2] << 8) + val[3]
# print"%02x" % Y1
