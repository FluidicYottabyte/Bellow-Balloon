
from ublox_gps import UbloxGps
import serial
import time

# Can also use SPI here - import spidev
# I2C is not supported

  
  
class GPSUnit:
    def __init__(self,setPort): #usually set it to: /dev/ttyS0
        self.port = serial.Serial(setPort, baudrate=9600, timeout=1)
        self.gps = UbloxGps(self.port)
        
    def getLocation(self):
      coords = self.gps.geo_coords()
      return((coords.lat,coords.lon,coords.height))
    
    def getExactTime(self):
      coords = self.gps.geo_coords()
      
      #in decreasing order from biggest to smallest measurement of time
      return((coords.year,coords.month,coords.day,coords.hour,coords.min,coords.sec)) 