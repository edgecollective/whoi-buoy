# CircuitPython Demo - USB/Serial echo

import board,busio,digitalio,time
#import busio
#import digitalio
#import time

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

while True:

    attempt=attempt + 1

    uart.write(b"AT+CSQ\r")
    #uart.write(b"AT\r")
    time.sleep(.1)
    a=uart.read(32).decode("utf-8").split()
    if len(a)==3:
        out=a[1].split(":")
        print(out)
        if len(out)==2:
            sig = int(out[1])
            #print(sig)
            print((sig,))
        #oled.fill(0)
        #oled.text(str(attempt),0,0,True)
        #oled.text(sig,0,8,True)
        #oled.show()
    time.sleep(1)