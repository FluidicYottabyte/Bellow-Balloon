# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# This example shows using two TSL2491 light sensors attached to TCA9548A channels 0 and 1.
# Use with other I2C sensors would be similar.
import time
import board
from SensorModules import WatPresSens

#Multiplexor Libary
import adafruit_tca9548a

# Create I2C bus as normal
i2c = board.I2C()  # uses board.SCL and board.SDA

# Create the TCA9548A object and give it the I2C bus
tca = adafruit_tca9548a.TCA9548A(i2c)

# Define the pressure sensor at the 3rd I2C bus
PresSens = WatPresSens.PressureSensor(tca[3])

# After initial setup, can just use sensors as normal.
while True:
    print("Pressure: "+str(PresSens.readTemp()))
    print("Temperature: "+str(PresSens.readPres()))
    time.sleep(0.1)
