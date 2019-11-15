# CircuitPython Demo - USB/Serial echo

import board
import busio
import digitalio
import time

#led = digitalio.DigitalInOut(board.D13)
#led.direction = digitalio.Direction.OUTPUT


# TX, RX
uart_gps = busio.UART(board.A2, board.A3, baudrate=9600)


while True:
    data = uart_gps.read(32)
    if data is not None:
        datastr = ''.join([chr(b) for b in data]) # convert bytearray to string
        print(datastr)
        print(datastr.split(','))
    time.sleep(.1)
