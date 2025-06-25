# RGB LED
# Date: 2025-6-25
# Describe: Red, green, blue alternate display

import time
import board
import neopixel

import digitalio,microcontroller

#Turn on the power of the peripherals
pw = digitalio.DigitalInOut(microcontroller.pin.P1_10)
pw.direction = digitalio.Direction.OUTPUT
pw.value = 1
time.sleep(0.5) 

#RGB LED
pixels = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.1, auto_write=False)

while True:

    #RED
    pixels.fill((255, 0, 0))
    pixels.show()
    time.sleep(1)

    #GREEN
    pixels.fill((0, 255, 0))
    pixels.show()
    time.sleep(1)

    #BLUE
    pixels.fill((0, 0, 255))
    pixels.show()
    time.sleep(1)
