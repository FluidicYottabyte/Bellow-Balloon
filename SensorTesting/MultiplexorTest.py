# SPDX-FileCopyrightText: 2021 Carter Nelson for Adafruit Industries
# SPDX-License-Identifier: MIT

# This example shows using TCA9548A to perform a simple scan for connected devices
import MultiplexorWithSensors
import time

Sensors = MultiplexorWithSensors.Multiplexor()

while True:
    print(Sensors.gravity())
    time.sleep(.1)
    