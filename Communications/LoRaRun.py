# SPDX-FileCopyrightText: 2018 Brent Rubell for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
Wiring Check, Pi Radio w/RFM9x

Learn Guide: https://learn.adafruit.com/lora-and-lorawan-for-raspberry-pi
Author: Brent Rubell for Adafruit Industries
"""
import time
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
# Import the SSD1306 module.
# Import the RFM9x radio module.
import adafruit_rfm9x

# Configure RFM9x LoRa Radio
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
rfm9x.tx_power = 23
prev_packet = None

while True:
    """packet = rfm9x.receive()
    if packet is None:
        print("Awaiting packet")
        time.sleep(.1)
    else:
        # Display the packet text and rssi
        prev_packet = packet
        packet_text = str(prev_packet, "utf-8")
        print(f'RX: {packet_text}')
        time.sleep(1)"""
        
    rfm9x.send(bytes("Test success\r\n","utf-8"))
    time.sleep(1)
