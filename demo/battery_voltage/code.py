# Battery Voltage
# Data: 2025-6-25

import time
import board
from analogio import AnalogIn

adc = AnalogIn(board.AREF) #锂电池电压

while True:
    
    print(round(adc.value*1.8/65535*4,2),'V')
    time.sleep(1) #1s


