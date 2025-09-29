# NRF UART
# Describe: Serial port data transmission and reception (IO voltage 1.8V)


import board,time
import busio

import digitalio,microcontroller

# k230 power
per = digitalio.DigitalInOut(microcontroller.pin.P0_28)
per.direction = digitalio.Direction.OUTPUT
per.value = 1

time.sleep(1)

#UART initialization
uart = busio.UART(board.TX, board.RX, baudrate=115200)

#Send data, requires byte array
uart.write(b'Hello World!')

while True:

    data = uart.readline()  #Receiving Data

    if data != None: #got data
        print(data)    #REPL print
        uart.write(data) #Data send back
