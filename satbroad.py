# CircuitPython Demo - USB/Serial echo

import board,busio,digitalio,time
#import busio
#import digitalio
#import time

led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

uart = busio.UART(board.TX, board.RX, baudrate=19200)


uart.write(b"AT\r")
time.sleep(.1)
a=uart.read(32)
print(a)
time.sleep(1)

uart.write(b"AT&K0\r")
time.sleep(.1)
a=uart.read(32)
print(a)
time.sleep(1)

uart.write(b"AT+SBDWT=Hello Somerville\r")
time.sleep(.1)
a=uart.read(32)
print(a)
time.sleep(1)


uart.write(b"AT+SBDIX\r")
time.sleep(.1)

while True:
    a=uart.read(32)
    print(a)
    time.sleep(1)