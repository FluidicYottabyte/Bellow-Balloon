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

    Rad.enable_crc = True
    Rad.tx_power = 23
    
    #Rad.auto_agc = True
    onPi = True
    
counter = 0

outgoing = PriorityQueue()
images = PriorityQueue()

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
                Rad.node = 1
                Rad.destination = 2
            else:
                Rad.node = 2
                Rad.destination = 1
            
            print(f"Node: {Rad.node}")
            print(f"Destination: {Rad.destination}")
        self.counter = 0
        
    def split_string_to_byte_chunks(self, s: str, byte_limit: int = 200) -> list:
        """
        Splits the input string into chunks such that when each chunk is encoded to bytes,
        it does not exceed the byte limit.

        :param s: The input string to be split.
        :param byte_limit: The maximum byte size for each chunk when encoded to bytes. Default is 252.
        :return: A list of string chunks.
        """
        chunks = []
        current_chunk = []
        current_chunk_byte_size = 0

        for char in s:
            char_byte_size = len(char.encode('utf-8'))
            if current_chunk_byte_size + char_byte_size > byte_limit:
                chunks.append(''.join(current_chunk))
                current_chunk = [char]
                current_chunk_byte_size = char_byte_size
            else:
                current_chunk.append(char)
                current_chunk_byte_size += char_byte_size

        if current_chunk:
            chunks.append(''.join(current_chunk))

        return chunks
        
    def test(self):
        return(Rad.send_with_ack(b"TEST"))
        
    def getQueue(self):
        return(outgoing)
    
    def addQueueImage(self,priority,object):
        images.put(object,priority)
        
    def addQueue(self,priority,object):
        outgoing.put(object,priority)
        
    def sendImg(self):
        SizeStat = not (images.empty())
        print(SizeStat)
        if SizeStat:
            CurrTask = images.get()
            print(CurrTask)
            path = os.getcwd()
            path = os.path.dirname(path)
        
            with open(os.path.join(os.path.join(path, "Communications"),CurrTask), "rb") as image:
                f = image.read()
                b = bytearray(f)
                print(b)
                #add send fuction
            return True
        else:
            return False
        
    def send(self):
        if not (outgoing.empty()):
            actualObject = outgoing.get()
            listedObj = self.split_string_to_byte_chunks(actualObject)
            
            for i, chunk in enumerate(listedObj):
                print(chunk)
                bytesObject = bytes(chunk.format(self.counter,Rad.node),"UTF-8")
                print(f"Sending raw: {bytesObject}")
                Rad.send(bytesObject)
                self.counter = self.counter + 1

    def receive(self):
        packet = Rad.receive(with_header=True)
        if packet is not None:
            print("Received (raw header):", [hex(x) for x in packet[0:4]])
            print("Received (raw payload): {0}".format(packet[4:]))
            print("Received RSSI: {0}".format(Rad.last_rssi))
            return(format(packet[4:]))
        else:
            return(None)

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
        