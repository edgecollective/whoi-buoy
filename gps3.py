# CircuitPython Demo - USB/Serial echo

import board
import busio
import digitalio
import time

#led = digitalio.DigitalInOut(board.D13)
#led.direction = digitalio.Direction.OUTPUT


# TX, RX
uart_gps = busio.UART(board.A2, board.A3, baudrate=9600)

i2c = busio.I2C(board.SCL, board.SDA)
import adafruit_ssd1306
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

#uart_gps.write(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
#PMTK314,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
time.sleep(.1)

while True:
    data = uart_gps.readline()
    #data= uart_gps.read(64)
    if data is not None:
        #data_str = ''.join([chr(b) for b in data]) # convert bytearray to string
        data_str=str(data,'ascii').strip()
        #print(data_str)
        ds=data_str.split(',')
        print(ds)
        #oled.fill(0)
        #oled.text(ds[0],0,0,True)
        if(ds[0]=='$GPGGA'):
            t=ds[1]
            #fix=ds[2]
            lat=ds[2]
            lon=ds[4]
            print(ds)
            print("len=",len(ds))
            oled.fill(0)
            oled.text(t,0,8,True)
            #if(fix=='V'):
            #    oled.text('no fix',0,8,True)
            #else:
            oled.text(lat+","+lon,0,16,True)
            oled.show()
        #print(datastr.split(','))
    time.sleep(.1)