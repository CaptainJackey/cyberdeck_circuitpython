# SPDX-FileCopyrightText: Copyright (c) 2020 Bryan Siepert for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# Light Sensor OPT3001
# Date: 2025-6-25

import time
import board
from opt3001 import OPT3001

import digitalio,microcontroller

#Turn on the power of the peripherals
pw = digitalio.DigitalInOut(microcontroller.pin.P1_10)
pw.direction = digitalio.Direction.OUTPUT
pw.value = 1 

time.sleep(0.5)

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
sensor = OPT3001(i2c)

while True:
    print(sensor.lux)
    time.sleep(1)
