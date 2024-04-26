# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# https://learn.adafruit.com/adafruit-bme680-humidity-temperature-barometic-pressure-voc-gas/python-circuitpython

import time
import board
import adafruit_bme680



class PHTGSensor:
    
    def __init__(self, bus):
        print("Pressure, Humidity, Temperature, and Gas sensor called.")
    
        self.bme680 = adafruit_bme680.Adafruit_BME680_I2C(bus,debug=False)
        
        self.bme680.sea_level_pressure = 1013.25
        self.temperature_offset = -5

    def readTemp(self):
        return(self.bme680.temperature + self.temperature_offset) # in degrees celsius
    
    def readPres(self):
        return(self.bme680.pressure) # in  hPa.  1hPa = 1mb
    
    def readHumid(self):
        return(self.bme680.relative_humidity) # 0-%100 I think 
    
    def readAlt(self):
        return(self.bme680.altitude) #In meters
    
    def readGas(self):
        return(self.bme680.gas) #Provides the Resistivity of the gas, proportional to VOC particles