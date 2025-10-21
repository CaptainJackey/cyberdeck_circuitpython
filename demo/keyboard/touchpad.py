import time
import board
import busio
import digitalio
import microcontroller

# periph power
per = digitalio.DigitalInOut(microcontroller.pin.P1_10)
per.direction = digitalio.Direction.OUTPUT
per.value = 1

time.sleep(0.5)

TOUCHPAD_ADDR = 0x33 #Q20 use 0x3b

REG_PID = 0x00
REG_REV = 0x01
REG_MOTION = 0x02
BIT_MOTION_MOT = 0x80
BIT_MOTION_OVF = 0x10
REG_DELTA_X = 0x03
REG_DELTA_Y = 0x04
REG_SQUAL = 0x05
REG_ORIENTATION = 0x77
BIT_ORIENTATION_X_INV = 0x20
BIT_ORIENTATION_Y_INV = 0x40

i2c = busio.I2C(microcontroller.pin.P0_11, microcontroller.pin.P0_12)

int_pin = digitalio.DigitalInOut(microcontroller.pin.P1_13)
int_pin.direction = digitalio.Direction.INPUT
int_pin.pull = digitalio.Pull.UP

# BB9900 needs to have TP_RESET pull-up input
# https://github.com/stolen/blackberry_trackpad
tp_reset = digitalio.DigitalInOut(microcontroller.pin.P1_12)
tp_reset.direction = digitalio.Direction.INPUT
tp_reset.pull = digitalio.Pull.UP

tp_shutdown = digitalio.DigitalInOut(microcontroller.pin.P1_11)
tp_shutdown.direction = digitalio.Direction.OUTPUT
tp_shutdown.value = 0

def read_register(reg, length=1):
    while not i2c.try_lock():
        pass
    i2c.writeto_then_readfrom(TOUCHPAD_ADDR, bytes([reg]), result := bytearray(length))
    i2c.unlock()
    return result if length > 1 else result[0]

def write_register(reg, value):
    while not i2c.try_lock():
        pass
    i2c.writeto(TOUCHPAD_ADDR, bytes([reg, value]))
    i2c.unlock()
    time.sleep(0.01)

def init_touchpad():
    print("Initializing touchpad...")

    product_id = read_register(REG_PID)
    revision = read_register(REG_REV)
    print(f"Touchpad ID: {product_id}, Revision: {revision}")

    # Invert X motion
    val = read_register(REG_ORIENTATION)
    write_register(REG_ORIENTATION, val | BIT_ORIENTATION_X_INV)

    print("Touchpad ready")

def read_motion():
    motion = read_register(REG_MOTION)

    if motion & BIT_MOTION_OVF:
        read_register(REG_DELTA_X)
        read_register(REG_DELTA_Y)
        return None

    if motion & BIT_MOTION_MOT:
        x = read_register(REG_DELTA_X)
        y = read_register(REG_DELTA_Y)

        squal = read_register(REG_SQUAL)
        print(f"Touchpad motion: X={x}, Y={y}, Quality={squal}")

init_touchpad()

while True:
    if not int_pin.value:
        read_motion()
    time.sleep(0.01)