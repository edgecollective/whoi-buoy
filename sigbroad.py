# CircuitPython Demo - USB/Serial echo

import board,busio,digitalio,time
#import busio
#import digitalio
#import time

THRESHOLD = 2
NUMCOUNTS = 3

led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

i2c = busio.I2C(board.SCL, board.SDA)
import adafruit_ssd1306
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

uart = busio.UART(board.TX, board.RX, baudrate=19200)

oled.fill(0)
oled.text("test",0,0,True)
oled.show()

attempt = 0

goodcount= 0

while True:

    attempt=attempt + 1

    uart.write(b"AT+CSQ\r")
    #uart.write(b"AT\r")
    time.sleep(.1)
    #a=uart.readline()
    #b=uart.readline()
    #c=uart.readline()
    #print(a,b,c)
    a=uart.read(64).decode("utf-8").split()
    #print(a)
    if len(a)==3:
        out=a[1].split(":")
        #print(out)
        if len(out)==2:
            sig = int(out[1])
            oled.fill(0)
            oled.text("a: "+str(attempt)+", s: "+str(sig),0,0,True)
            oled.text("t: "+str(THRESHOLD)+", g: "+str(goodcount),0,8,True)
            #oled.text("goodcount: "+str(goodcount),0,16,True)
            oled.show()
            print((sig,))
            if(sig>=THRESHOLD):
                goodcount=goodcount+1
            else:
                goodcount = 0 #reset
    if (goodcount > NUMCOUNTS):

        uart.write(b"AT&K0\r")
        time.sleep(.1)
        a=uart.read(32)
        print(a)
        time.sleep(1)

        uart.write(b"AT+SBDWT=Hello " + str(attempt) + "\r")
        time.sleep(.1)
        a=uart.read(32)
        print(a)
        time.sleep(1)


        uart.write(b"AT+SBDIX\r")
        print("sent!")
        oled.text("sent!",0,16,True)
        oled.show()

        while True:
            a=uart.read(32)
            print(a)
            time.sleep(1)

        goodcount=0

        time.sleep(60)


