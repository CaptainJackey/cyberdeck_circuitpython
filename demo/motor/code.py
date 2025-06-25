# DRV2604 Motor Control
# Date: 2025-6-25

import time
import board
import busio
import digitalio
import microcontroller

#Turn on the power of the peripherals
pw = digitalio.DigitalInOut(microcontroller.pin.P1_10)
pw.direction = digitalio.Direction.OUTPUT
pw.value = True  
time.sleep(0.5) 

DRV2604_ADDR = 0x58

DRV2604_MODE = 0x01
DRV2604_RTP_INPUT = 0x02
DRV2604_GO = 0x0C

i2c = busio.I2C(microcontroller.pin.P0_11, microcontroller.pin.P0_12)

lra_en = digitalio.DigitalInOut(microcontroller.pin.P1_07)
lra_en.direction = digitalio.Direction.OUTPUT

def write_register(reg, value):
    while not i2c.try_lock():
        pass
    i2c.writeto(DRV2604_ADDR, bytes([reg, value]))
    i2c.unlock()
    time.sleep(0.01)

print("Vibrating for 1 second")

lra_en.value = True
time.sleep(0.1)

write_register(DRV2604_MODE, 0x05)
write_register(DRV2604_RTP_INPUT, 127)
write_register(DRV2604_GO, 1)

time.sleep(1)

write_register(DRV2604_RTP_INPUT, 0)
write_register(DRV2604_GO, 0)

lra_en.value = False