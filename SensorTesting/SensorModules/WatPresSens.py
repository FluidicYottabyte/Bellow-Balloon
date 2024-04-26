# SPDX-FileCopyrightText: 2019 Bryan Siepert, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
import time
import board
import adafruit_lps35hw

class PressureSensor:
    
    def __init__(self, bus):
        print("Pressure sensor called.")
    
        self.lps = adafruit_lps35hw.LPS35HW(bus)

    def readTemp(self):
        return(self.lps.temperature)
    
    def readPres(self):
        return(self.lps.pressure)
