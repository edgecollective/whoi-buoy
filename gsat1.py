# CircuitPython Demo - USB/Serial echo

import board, busio, digitalio, time

#led = digitalio.DigitalInOut(board.D13)
#led.direction = digitalio.Direction.OUTPUT
GPS_RETRY_PERIOD = 10 # seconds
GPS_MAX_ATTEMPTS = 20

SAT_RETRY_PERIOD = 5
SAT_MAX_ATTEMPTS = 30
SAT_RESPONSE_THRESHOLD = 30 # seconds
SAT_SIGNAL_THRESHOLD = 3
GOODCOUNT_THRESHOLD = 4

# TX, RX
uart_gps = busio.UART(board.A2, board.A3, baudrate=9600)

uart_sat = busio.UART(board.TX, board.RX, baudrate=19200)


i2c = busio.I2C(board.SCL, board.SDA)
import adafruit_ssd1306
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

trialcount= 0
got_fix = False

## try to get a gps fix
lat = 'NA'
lon = 'NA'

oled.fill(0)

try:

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
                oled.text("GPS fix attempt #"+str(trialcount),0,0,True)
                oled.show()
                trialcount = trialcount + 1
                t=sp[1]
                status=sp[2]
                print("----",sp)
                if (status=='A'):
                    print("got gps fix")
                    #oled.text("got gps fix!",0,8,True)
                    #oled.show()
                    #time.sleep(2)
                    got_fix=True
                    lat = sp[3]
                    lon = sp[5]
                else:
                    print("no gps fix ... ")
                    time.sleep(GPS_RETRY_PERIOD)

except Exception as e:
    print("error: "+str(e))

print("lat = ", lat, "lon = ", lon)

# get parameters here
temp = 25.
humidity = 33.
pressure = 32.
probe= 10.


trialcount= 0
got_fix = False
goodcount = 0

try:
    while ((trialcount < SAT_MAX_ATTEMPTS) and (got_fix == False)):
        trialcount=trialcount+1
        print("trialcount = ", trialcount)
        uart_sat.write(b"AT+CSQ\r")
        reply=False
        initial_time = time.monotonic()
        current_time = time.monotonic()
        elapsed = time.monotonic() - initial_time # seconds

        sig = 'NA'
        while ((reply==False) and (elapsed < SAT_RESPONSE_THRESHOLD)):
            elapsed = time.monotonic() - initial_time
            #print("elapsed=",elapsed)
            a=uart_sat.readline()
            #print(a)

            if a is not None:
                try:
                    out=a.decode("utf-8").strip().split(":")
                    #print(out)
                    if len(out)==2:
                        sig=out[1]
                        reply=True
                        #print("signal=",sig)
                except OSError:
                    pass
                except RuntimeError:
                    pass

        oled.fill(0)
        oled.text("sat fix attempt #"+str(trialcount),0,0,True)
        oled.text("signal str = "+str(sig),0,8,True)
        oled.text("goodcount = "+str(goodcount),0,16,True)
        oled.show()

        if (int(sig) >= SAT_SIGNAL_THRESHOLD):
            goodcount = goodcount + 1
        else:
            goodcount = 0

        print ("signal = ", sig, "; goodcount = ", goodcount)

        if (goodcount >= GOODCOUNT_THRESHOLD):
            got_fix = True
            print("got fix")

        time.sleep(SAT_RETRY_PERIOD)

except Exception as e:
    print("error: "+str(e))

if (got_fix == True):

    oled.fill(0)
    oled.text("Sat send ...",0,0,True)
    oled.show()
    # then send the data
    uart_sat.write(b"AT&K0\r")
    a=uart_sat.read(32)
    print(a)
    time.sleep(1)

    # get parameters here
    temp = 25.1
    humidity = 33.
    pressure = 32.
    probe= 10.3

    sendstr = str(lat)+","+str(lon)+","+str(temp)+","+str(probe)+","+str(humidity)+","+str(pressure)

    uart_sat.write(b"AT+SBDWT="+sendstr+"\r")
    a=uart_sat.readline()
    print(a)
    time.sleep(1)

    uart_sat.write(b"AT+SBDIX\r")

    confirmed = False
    while (confirmed == False):
        a=uart_sat.readline()
        if a is not None:
            print(a)
            try:
                res=a.decode("utf=8").strip()
                res1=res.split(":")
                print(res)
                print(res1)
                if len(res1)==2:
                    if(res1[0]=='+SBDIX'):

                        res2=res1[1].split(",")
                        status=res2[0]
                        print("status=",status)
                        if (int(status)==0):
                            print("confirmed!")
                        confirmed=True
            except OSError:
                pass
            except RuntimeError:
                pass
        time.sleep(1)

    oled.text("status ="+str(status),0,8,True)
    oled.show()
    time.sleep(3)
    print("PULL DONE")
    # pull DONE pin and sleep

else:
    oled.fill(0)
    oled.text("Never got sat fix.",0,0,True)
    oled.show()
    print ("never got a satellite fix")
    print ("PULL DONE")
    # pull DONE pin and sleep