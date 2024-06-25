
from ublox_gps import UbloxGps
import serial
import time

# Can also use SPI here - import spidev
# I2C is not supported

port = serial.Serial('/dev/ttyS0', baudrate=9600, timeout=1)
gps = UbloxGps(port)

def run():
  try: 
    print("Listening for UBX Messages.")
    while True:
      try: 
        coords = gps.geo_coords()
        print(coords)
      except (ValueError,AttributeError) as err:
        print(err)
      except (IOError) as err:
        print("Resetting port")
        port.close()
        time.sleep(1)
        port.open()
  
  finally:
    port.close()

if __name__ == '__main__':
  run()
  
  
class GPSUnit:
    def __init__(self,setPort): #usually set it to: /dev/ttyS0
        self.port = serial.Serial(setPort, baudrate=9600, timeout=1)
        self.gps = UbloxGps(port)
        
    def getLocation(self):
      coords = self.gps.get_coords()
      return((coords.lat,coords.lon,coords.height))
    
    def getExactTime(self):
      coords = self.gps.get_coords()
      
      #in decreasing order from biggest to smallest measurement of time
      return((coords.year,coords.month,coords.day,coords.hour,coords.min,coords.sec)) 