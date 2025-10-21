import board
import digitalio
import time
import microcontroller
import busio
import bitbangio

#Turn on the power of the peripherals
pw = digitalio.DigitalInOut(microcontroller.pin.P1_10)
pw.direction = digitalio.Direction.OUTPUT
pw.value = 1 

time.sleep(0.5)

# Turn on keyboard's backlight
ds = digitalio.DigitalInOut(microcontroller.pin.P1_15)
ds.direction = digitalio.Direction.OUTPUT
ds.value = 1

while True:
    pass