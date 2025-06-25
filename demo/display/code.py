# Display with backlight on
# Date: 2025-6-25

import busio
import digitalio
import time
import microcontroller

#Turn on the power of the peripherals
pw = digitalio.DigitalInOut(microcontroller.pin.P1_10)
pw.direction = digitalio.Direction.OUTPUT
pw.value = 1
time.sleep(0.5)

# Turn on bakclight
ds = digitalio.DigitalInOut(microcontroller.pin.P1_06)
ds.direction = digitalio.Direction.OUTPUT
ds.value = 1

WIDTH = 400
HEIGHT = 240
BYTES_PER_LINE = WIDTH // 8

disp = digitalio.DigitalInOut(microcontroller.pin.P0_02)
disp.direction = digitalio.Direction.OUTPUT
disp.value = 1

ds = digitalio.DigitalInOut(microcontroller.pin.P1_05)
ds.direction = digitalio.Direction.OUTPUT
ds.value = 0

spi = busio.SPI(clock=microcontroller.pin.P0_05, MOSI=microcontroller.pin.P0_04)
cs = digitalio.DigitalInOut(microcontroller.pin.P0_27)
cs.direction = digitalio.Direction.OUTPUT

extcom = digitalio.DigitalInOut(microcontroller.pin.P1_04)
extcom.direction = digitalio.Direction.OUTPUT
extcom.value = 0

CMD_CLEAR = 0x20
CMD_WRITE = 0x80
CMD_VCOM = 0x40

while not spi.try_lock():
    pass

spi.configure(baudrate=1000000, phase=0, polarity=0)

def clear_display():
    print("clear display")
    cs.value = 1
    spi.write(bytearray([CMD_CLEAR]))
    spi.write(bytearray([0x00])) 
    cs.value = 0

def toggle_vcom():
    print("toggle vcom")
    cs.value = 1
    spi.write(bytearray([CMD_VCOM]))
    spi.write(bytearray([0x00]))
    cs.value = 0

def draw_checkerboard(flip):

    cs.value = 1
    spi.write(bytearray([CMD_WRITE]))
    for y in range(HEIGHT):
        line_data = bytearray(BYTES_PER_LINE)
        for x in range(BYTES_PER_LINE):

            if (x // 4 + y // 8) % 2 == 0:
                line_data[x] = 0xff if flip else 0x00
            else:
                line_data[x] = 0x00 if flip else 0xff
            
            spi.write(bytearray([y + 1]))
            spi.write(line_data)
            spi.write(bytearray([0x00]))
    
    spi.write(bytearray([0x00]))
    cs.value = 0

clear_display() #clear
time.sleep(0.1)

toggle_vcom()

draw_checkerboard(0)

while True:
    pass