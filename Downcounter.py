# Import MicroPython libraries of PIN and SPI
from machine import Pin, SPI

# Import MicoPython max7219 library
import max7219

# Import time
import time

#Intialize the SPI
spi = SPI(0, baudrate=10000000, polarity=1, phase=0,
          sck=Pin(2), mosi=Pin(3))

ss = Pin(5, Pin.OUT)

# Create matrix display instant
display = max7219.Matrix8x8(spi, ss, 4)

# Brightness 1-15
display.brightness(1)

while True:
    for i in range(1000,0,-1):
    # ----- ABC -----
        text=f'{i:4d}'
        display.fill(0)
        display.text(text, 0, 0, 1)
        display.show()
        time.sleep(.3)
