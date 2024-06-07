# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# This example shows using two TSL2491 light sensors attached to TCA9548A channels 0 and 1.
# Use with other I2C sensors would be similar.
import time
import board
import os
import sys

path = os.getcwd()
path = os.path.dirname(path)
path = os.path.join(path,"SensorTesting")
sys.path.insert(0, path)
print(path)


from SensorModules import WatPresSens
from SensorModules import PHTCSens
from SensorModules import IMUSens

#Multiplexor Libary
import adafruit_tca9548a

# Create I2C bus as normal
i2c = board.I2C()  # uses board.SCL and board.SDA
#i2c3 = board.I2C(board.SCL3,board.SDA3)
#PosSens = IMUSens.IMU(i2c)

"""^^^^^^^^^^^^^^FIGURE OUT HOW TO ACCESS I2C-3^^^^^^^^^^^^^"""

# Create the TCA9548A object and give it the I2C bus
tca = adafruit_tca9548a.TCA9548A(i2c)

# Define the pressure sensor at the 3rd I2C bus

PresSens = WatPresSens.TPSensor(tca[3])
EvrySens = PHTCSens.PHTGSensor(tca[2])


# Create a class to read sensor information
class Multiplexor:

    def __init__(self):
        print("Multiplexor called.")

        self.tca = adafruit_tca9548a.TCA9548A(i2c)

    def avgTemp(self):
        avg = (PresSens.readTemp() + EvrySens.readTemp()) / 2
        return(avg)
    
    def readPres(self):
        return(EvrySens.readPres())
    
    def altCheck(self):
        if EvrySens.readAlt() >= 38000:
            return(True)
        else:
            return(False)
        
    def getHumid(self):
        return(EvrySens.readHumid())