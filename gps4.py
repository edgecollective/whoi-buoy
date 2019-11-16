# CircuitPython Demo - USB/Serial echo

import board, busio, digitalio, time

#led = digitalio.DigitalInOut(board.D13)
#led.direction = digitalio.Direction.OUTPUT
GPS_RETRY_PERIOD = 10 # seconds
GPS_MAX_ATTEMPTS = 10

# TX, RX
uart_gps = busio.UART(board.A2, board.A3, baudrate=9600)

i2c = busio.I2C(board.SCL, board.SDA)
import adafruit_ssd1306
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

trialcount= 0
got_fix = False

## try to get a gps fix
lat = 'NA'
lon = 'NA'

while ((trialcount < GPS_MAX_ATTEMPTS) and (got_fix == False)):
    data = uart_gps.readline()
    #data= uart_gps.read(64)
    if data is not None:
        dec=data.decode("utf-8").strip()
        #print(dec)
        sp = dec.split(",")
        #print(sp)
        if (sp[0]=="$GPRMC"):
            print("count=",trialcount)
            trialcount = trialcount + 1
            t=sp[1]
            status=sp[2]
            print("----",sp)
            if (status=='A'):
                print("got fix")
                got_fix=True
                lat = sp[3]
                lon = sp[5]
            else:
                print("no fix ... ")
                time.sleep(GPS_RETRY_PERIOD)

print("lat = ", lat, "lon = ", lon)
