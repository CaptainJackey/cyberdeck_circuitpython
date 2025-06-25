# Speaker
# Date: 2025-6-25

import time
import microcontroller
import busio
import audiobusio
import audiocore
import array
import math

import digitalio,microcontroller

# periph power
per = digitalio.DigitalInOut(microcontroller.pin.P1_10)
per.direction = digitalio.Direction.OUTPUT
per.value = 1

time.sleep(0.5)

DA7212_I2C_ADDR = 0x1A

i2c = busio.I2C(microcontroller.pin.P0_11, microcontroller.pin.P0_12)

def write_register(register, value):
    while not i2c.try_lock():
        pass
    i2c.writeto(DA7212_I2C_ADDR, bytes([register, value]))
    i2c.unlock()
    time.sleep(0.01)

def read_register(register):
    while not i2c.try_lock():
        pass
    i2c.writeto_then_readfrom(DA7212_I2C_ADDR, bytes([register]), result_buffer := bytearray(1))
    i2c.unlock()
    return result_buffer[0]

# Initialize DA7212 (basic power-up sequence)
write_register(0x1D, 0x80) # Reset DA7212
write_register(0x92, 0x00) # Set ramp rate to default nominal / 8 ~1/128s
write_register(0x23, 0x08) # Enable master bias
time.sleep(0.040)
write_register(0x90, 0x80) # Enable digital ldo
write_register(0x29, 0xc0) # Enable AIF 16 bit i2s
write_register(0x94, 0x02) # Resync clock on drift
write_register(0x40, 0x80) # Filter 5 enable soft mute
write_register(0x2a, 0x32) # R source: 3 L source: 2
write_register(0x4b, 0x08) # Mix out left source: DAC_L
write_register(0x4c, 0x08) # Mix out right source: DAC_R

# Speaker
write_register(0x4a, 0x3a) # Speaker gain to 10dB
write_register(0x69, 0x80) # Enable DAC L
write_register(0x6a, 0x80) # Enable DAC R
write_register(0x6d, 0xa8) # Enable speaker
write_register(0x6e, 0x88) # Mix out L
write_register(0x6f, 0x88) # Mix out R
write_register(0x51, 0xc9) # System mode: DAC, speaker enable

# Headphone
'''
write_register(0x47, 0xf1) # Charge pump control set
write_register(0x95, 0x36) # Charge pump threshold set
write_register(0x96, 0xa5) # Charge pump delay set
write_register(0x48, 0x39) # Headphone L gain 0dB
write_register(0x49, 0x39) # Headphone R gain 0dB
write_register(0x69, 0x80) # Enable DAC L
write_register(0x6a, 0x80) # Enable DAC R
write_register(0x6b, 0xa8) # Headphone L enable
write_register(0x6c, 0xa8) # Headphone R enable
write_register(0x6e, 0x88) # Mix out L
write_register(0x6f, 0x88) # Mix out R
write_register(0x51, 0xf1) # System mode: DAC, headphone enable
'''

write_register(0xb5, 0x60) # Enable tone generator
time.sleep(0.040)
write_register(0x40, 0x00) # Filter 5 disable soft mute

BCLK = microcontroller.pin.P1_09
LRCLK = microcontroller.pin.P0_08
DIN = microcontroller.pin.P0_07
DOUT = microcontroller.pin.P1_08
MCLK = microcontroller.pin.P0_06

i2s = audiobusio.I2SOut(BCLK, LRCLK, DOUT)

SAMPLE_RATE = 48000
FREQUENCY = 440
AMPLITUDE = 32767

samples = array.array("h", [
    int(math.sin(2 * math.pi * FREQUENCY * i / SAMPLE_RATE) * AMPLITUDE)
    for i in range(SAMPLE_RATE // FREQUENCY)
])

wave = audiocore.RawSample(samples, sample_rate=SAMPLE_RATE)

print("Playing Test Tone")
i2s.play(wave, loop=True)
time.sleep(5) # play 5s
write_register(0x4a, 0x00) # close speaker
time.sleep(1)
i2s.stop()
print("Done")