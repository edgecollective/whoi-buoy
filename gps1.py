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
    data = uart_gps.readline()
    #data= uart_gps.read(64)
    if data is not None:
        #data_str = ''.join([chr(b) for b in data]) # convert bytearray to string
        data_str=str(data,'ascii').strip()
        #print(data_str)
        ds=data_str.split(',')
        #print(ds)
        if(ds[0]=='GPRMC'):
            print(ds)
            print("len=",len(ds))
        #print(datastr.split(','))
    time.sleep(.1)
