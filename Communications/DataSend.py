# SPDX-FileCopyrightText: 2018 Brent Rubell for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
Wiring Check, Pi Radio w/RFM9x

Learn Guide: https://learn.adafruit.com/lora-and-lorawan-for-raspberry-pi
Author: Brent Rubell for Adafruit Industries
"""
import time
import os
from queue import PriorityQueue

path = os.getcwd()

print(os.path.dirname(os.path.dirname(os.path.dirname(path))))

#checks if it is on pi or not. Remove completely on launch

onPi = False

if os.path.dirname(os.path.dirname(os.path.dirname(path))) == "/home":
    print("on Pi")
    import busio
    from digitalio import DigitalInOut, Direction, Pull
    import board

    import adafruit_rfm9x

    # Configure RFM9x LoRa Radio
    CS = DigitalInOut(board.CE1)
    RESET = DigitalInOut(board.D25)
    spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
    Rad = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)

    Rad.tx_power = 23
    Rad.ack_wait = 1
    Rad.ack_retries = 2
    Rad.coding_rate = 5
    
    Rad.auto_agc = True
    onPi = True

outgoing = PriorityQueue()

from queue import PriorityQueue
# Import the SSD1306 module.
# Import the RFM9x radio module.




class Radio:
    
    def __init__(self, Balloon):
        if onPi:
            print("Begin radio object")
            Rad.reset()
            Rad.spreading_factor = 6
            print("Valid bandwidth:"+str(Rad.bw_bins))
            if Balloon:
                Rad.node = 66
                Rad.destination = 65
            else:
                Rad.node = 65
                Rad.destination = 66
        
    def test(self):
        return(Rad.send_with_ack(b"TEST"))
        
    def getQueue(self):
        return(outgoing)
    
    def addQueue(self,priority,object):
        outgoing.put(object,priority)
        
    def send(self):
        SizeStat = not (outgoing.empty())
        print(SizeStat)
        if SizeStat:
            CurrTask = outgoing.get()
            print(CurrTask)
        
            with open(os.path.join(os.path.join(os.getcwd(), "Communications"),CurrTask), "rb") as image:
                f = image.read()
                b = bytearray(f)
                print(b)
            return True
        else:
            return False

    def receive(self):
        receivedInfo = Rad.receive(keep_listening=False,with_ack=True,timeout=5.0)
        return(receivedInfo)

    #In the event of loss of contact, this function will run through all possible fixes
    
    def attemptFix(self):
        print("Attempting fix. Current SNR is: "+str(Rad.snr))
        print("First attempt, reset.")
        
        Rad.reset()
        
        if not self.test():
            print("Unable to make contact, continuing with fix.")
        else:
            print("Connection restored")
            
        #Begin by testing the spread 
        #(min 6, max 12. Higher value = lower bandwidth, but better connection)
        for i in range(Rad.spreading_factor,12):
            print("Testing spread: "+str(i))
            
            Rad.spreading_factor = i
            if self.test():
               print("Spread fixed, new spread is: " + str(i))
               return(True)
           
        print("Spread did not resolve, attempting bandwidth decrease.")
        
        for j in range(list.index(Rad.bw_bins,Rad.signal_bandwidth),0):
            print("Testing bandwidth: "+str(j))
            
            Rad.signal_bandwidth = j
            if self.test():
               print("Bandwidth resolved. New bandwidth is: " + str(j))
               return(True)
           
        print("Bandwidth did not resolve. changing coding rate.")
        
        #Coding rate is between 5 and 8 inclusive. Lower values mean worse error correction, but more info.
        for j in range(Rad.coding_rate,8):
            print("Testing bandwidth: "+str(j))
            
            Rad.signal_bandwidth = j
            if self.test():
               print("Bandwidth resolved. New bandwidth is: " + str(j))
               return(True)
           
        print("No fix possible. Radio is now left in searching state.")
        return(False)
        