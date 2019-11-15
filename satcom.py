# CircuitPython Demo - USB/Serial echo

import board
import busio
import digitalio
import time

led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

uart = busio.UART(board.TX, board.RX, baudrate=19200)

while True:
    #a=uart.read(32)
    #a=uart.read(32)
    #print(a)
    #time.sleep(1)
    uart.write(b"AT\r")
    time.sleep(.1)
    a=uart.read(32)
    print(a)
    time.sleep(1)
    #time.sleep(.1)
    #a=uart.read(32)
    #print(a)
    