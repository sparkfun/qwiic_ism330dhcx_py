#!/usr/bin/env python
#-------------------------------------------------------------------------------
# qwiic_ism330dhcx_ex3_sensor_hub.py
#
#   This example demonstrates the "sensor hub" feature of the ISM330DHCX. 
# 	The ISM330DHCX acts as a controller for external sensors connected to this 
# 	alternate bus (SDX/SCX). In this example, the ISM330DHCX is connected to the
# 	MMC5983MA Magnetometer. You might notice that we have a 9DoF with these two
# 	parts but not in this configuration. The reason is that the magnetometer requires
# 	an "initiate measurement" bit to be flipped before every reading, while this is
# 	possible (it's demonstrated below) it's also not ideal for this setup. A more
# 	ideal setup would be a sensor that is just turned on and data is pulled 
# 	periodically.
#-------------------------------------------------------------------------------
# Written by SparkFun Electronics, January 2025
#
# This python library supports the SparkFun Electroncis Qwiic ecosystem
#
# More information on Qwiic is at https://www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#===============================================================================
# Copyright (c) 2024 SparkFun Electronics
#
# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the "Software"), to deal 
# in the Software without restriction, including without limitation the rights 
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
# copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all 
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
# SOFTWARE.
#===============================================================================

import qwiic_ism330dhcx
import sys
import time

# 8 bit addressing is required for the 6DoF
# to communicate with its' external sensors.
kMagAddrRead = 0x61 # (0x30 << 1) | 1
kMagAddrWrite = 0x60 # (0x30 << 1)

kMagReadReg = 0x00 # Read from 0x00
kMagReadLen = 0x07 # Read seven times consecutively

# INT_CTRL0 (0x09) - contains the bit to initiate measurement.
# It must be written before each read and is cleared automatically.
kMagWriteReg = 0x09
kMagWriteData = 0x01 # Value to write to INT_CTRL0

# Create instance of device
myIsm = qwiic_ism330dhcx.QwiicISM330DHCX()

# TODO: should we move this function into the library?
def write_control_bit(address, subAddress, data):
	# Sensors must be off for sensor hugb configuration
	myIsm.set_accel_data_rate(myIsm.kXlOdrOff)
	myIsm.set_gyro_data_rate(myIsm.kGyroOdrOff)
	myIsm.enable_sensor_i2c(False)

	# Delay 300us until 6DoF I2C is powered down
	time.sleep(0.00031)

	# Configure a write
	myIsm.set_hub_sensor_write(address, subAddress, data)
	# Re-enable sensor for write
	myIsm.set_accel_data_rate(myIsm.kXlOdr104Hz)
	myIsm.enable_sensor_i2c(True)
						 
	# Wait for write to complete
	while myIsm.get_hub_status() == False:
		time.sleep(1)
	
	# Turn off sensor
	myIsm.enable_sensor_i2c(False)
	time.sleep(0.00031)

def runExample():
	print("\nQwiic ISM330DHCX Example 3 - Sensor Hub\n")

	# Check if it's connected
	if myIsm.is_connected() == False:
		print("The device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	myIsm.begin()

	# Reset the device and the sensor hub to default settings. 
	# This is helpful if you're doing multiple uploads testing different settings. 
	myIsm.device_reset()
	myIsm.reset_sensor_hub()

	# Wait for it to finish resetting
	while myIsm.get_device_reset() == False:
		time.sleep(1)

	print("Reset.")
	print("Applying settings.")
	time.sleep(0.100)

	myIsm.set_device_config()
	myIsm.set_block_data_update()

	# Set the number of peripheral sensors to be read by the 6dof. By passing 0, we only enable slave 0
	myIsm.set_number_hub_sensors(0)
	# Enable Pullup resistors on the SDX and SCX lines
	myIsm.set_hub_pull_ups()
	# Output data rate for the external sensor
	myIsm.set_hub_odr(myIsm.kShOdr104Hz)

	# Send control bit to Magnetometer
	write_control_bit(kMagAddrWrite, kMagWriteReg, kMagWriteData)

	# Set read settings for external sensor 0. By passing 0, we only enable slave 0
	myIsm.set_hub_sensor_read(0, kMagAddrRead, kMagReadReg, kMagReadLen)

	# Enable the 6DoF as a controller I2C
	# All configurations to the sensor hub must occur while the controller I2C 
	# bus is powered down.
	myIsm.enable_sensor_i2c(True)

	# Apply accelerometer settings
	myIsm.set_accel_full_scale(myIsm.kXlFs4g)
	myIsm.set_accel_filter_lp2()
	myIsm.set_accel_slope_filter(myIsm.kLpOdrDiv100)

	# Apply gyroscope settings
	myIsm.set_gyro_full_scale(myIsm.kGyroFs500dps)
	myIsm.set_gyro_filter_lp1()
	myIsm.set_gyro_lp1_bandwidth(myIsm.kBwMedium)

	# Enable sensors
	myIsm.set_accel_data_rate(myIsm.kXlOdr104Hz)
	myIsm.set_gyro_data_rate(myIsm.kGyroOdr104Hz)

	while True:
		if myIsm.check_status():
			# Get the accelerometer data
			accelData = myIsm.get_accel()
			gyroData = myIsm.get_gyro()
			
			# If you've given the 6DoF the wrong address for the external sensor, this
			# bit will tell you. The zero argument is the external sensor to check (0-3).
			if myIsm.get_external_sensor_nack(0):
				print("External sensor 0 Nacked...")
			
			# Check if the sensor hub is finished
			if myIsm.get_hub_status():
				# Get the data stored in the 6DoF's registers.
				shRawData = myIsm.read_peripheral_sensor(kMagReadLen)

				# TODO: Should we add a function to the library to abstract away the below conversion?
				# Shift and convert the raw data 		
				magXVal = (shRawData[0] << 10) | (shRawData[1] << 2) | ((shRawData[6] >> 6) & 0x03)
				magYVal = (shRawData[2] << 10) | (shRawData[3] << 2) | ((shRawData[6] >> 4) & 0x03)
				magZVal = (shRawData[4] << 10) | (shRawData[5] << 2) | ((shRawData[6] >> 2) & 0x03)
				
				normalizedX = magXVal - 131072.0
				normalizedX = (normalizedX/131072.0) * 8

				normalizedY = magYVal - 131072.0
				normalizedY = (normalizedY/131072.0) * 8

				normalizedZ = magZVal - 131072.0
				normalizedZ = (normalizedZ/131072.0) * 8

				# Z axis between magnetometer and acclerometer are opposite. 
				normalizedZ = normalizedZ * (-1)

				print("Magnetometer X: %f, Y: %f, Z: %f\n" % (normalizedX, normalizedY, normalizedZ))

				# Send another bit to take more measurements
				write_control_bit(kMagAddrWrite, kMagWriteReg, kMagWriteData)
			
			print("Accel X: %f, Y: %f, Z: %f " % (accelData.xData, accelData.yData, accelData.zData), end='')
			print("Gyro X: %f, Y: %f, Z: %f" % (gyroData.xData, gyroData.yData, gyroData.zData))

		time.sleep(0.100) # Delay so that we don't spam user console or I2C bus

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example")
		sys.exit(0)