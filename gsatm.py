# CircuitPython Demo - USB/Serial echo

import board, busio, digitalio, time, adafruit_bme280
import adafruit_ssd1306

from analogio import AnalogIn

from adafruit_onewire.bus import OneWireBus
from adafruit_ds18x20 import DS18X20

""" GPS_RETRY_PERIOD = 3 # seconds
GPS_MAX_ATTEMPTS = 50

SAT_RETRY_PERIOD = 5
SAT_MAX_ATTEMPTS = 40
SAT_RESPONSE_THRESHOLD = 30 # seconds
SAT_SIGNAL_THRESHOLD = 3
GOODCOUNT_THRESHOLD = 4 """


GPS_RETRY_PERIOD = 1 # seconds
GPS_MAX_ATTEMPTS = 3

SAT_RETRY_PERIOD = 1
SAT_MAX_ATTEMPTS = 3
SAT_RESPONSE_THRESHOLD = 30 # seconds
SAT_SIGNAL_THRESHOLD = 3
GOODCOUNT_THRESHOLD = 4

def get_voltage(pin):
    return (pin.value * 3.3) / 65536

# Initialize one-wire bus on board pin D5.
ow_bus = OneWireBus(board.A1)



# done pin
done = digitalio.DigitalInOut(board.A5)
done.direction = digitalio.Direction.OUTPUT



# battery measurement pin1
batt_pin = AnalogIn(board.A0)


# TX, RX
uart_gps = busio.UART(board.A2, board.A3, baudrate=9600)

uart_sat = busio.UART(board.TX, board.RX, baudrate=19200)


i2c = busio.I2C(board.SCL, board.SDA)

bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)


oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

trialcount= 0
got_fix = False

## try to get a gps fix
lat = 'NA'
lon = 'NA'

oled.fill(0)




try:

    while ((trialcount < GPS_MAX_ATTEMPTS) and (got_fix == False)):
        try:

            data = uart_gps.readline()
            #data= uart_gps.read(64)
            if data is not None:
                dec=data.decode("utf-8").strip()
                #print(dec)
                sp = dec.split(",")
                #print(sp)
                if (sp[0]=="$GPRMC"):
                    print("count=",trialcount)
                    oled.fill(0)
                    oled.text("GPS fix attempt #"+str(trialcount),0,0,True)
                    oled.show()
                    trialcount = trialcount + 1
                    t=sp[1]
                    status=sp[2]
                    print("----",sp)
                    if (status=='A'):
                        print("got gps fix")
                        oled.text("got gps fix!",0,8,True)
                        oled.show()
                        time.sleep(2)
                        got_fix=True
                        lat = sp[3]
                        lon = sp[5]
                    else:
                        print("no gps fix ... ")
                        oled.text("(no gps fix yet)",0,8,True)
                        oled.show()
                        time.sleep(2)
                        time.sleep(GPS_RETRY_PERIOD)
        except Exception as e:
            print("error: "+str(e))

except Exception as e:
    print("error: "+str(e))

print("lat = ", lat, "lon = ", lon)

# get parameters here
temp = bme280.temperature
humidity = bme280.humidity
pressure = bme280.pressure
probe1=-99.
probe2=-99.

try:
    # Scan for sensors and grab the first one found.
    ds18_bus=ow_bus.scan()
    print(ds18_bus)
    ds18=[]
    for probe in ds18_bus:
        print(probe)
        ds18.append(DS18X20(ow_bus, probe))
    time.sleep(1)
    probe1=ds18[0].temperature
    probe2=ds18[0].temperature

    #probe2=float(ds18[1].temperature)
except Exception as e:
    print("error: "+str(e))

# battery voltage
batt_voltage = 2*float(get_voltage(batt_pin))



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
        oled.text("sig = "+str(sig)+" gc = "+str(goodcount),0,8,True)
        outline1 = "%0.1f,%0.1f,%0.1f,%0.1f" % (temp,humidity,pressure,batt_voltage)
        outline2 = "%0.1f,%0.1f" % (probe1,probe2)
        print(outline1)
        print(outline2)
        #oled.fill(0)
        oled.text(outline1,0,16,True)
        oled.text(outline2,0,24,True)
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

    sendstr = str(lat)+","+str(lon)+","+str(temp)+","+str(humidity)+","+str(pressure)+","+str(probe1)+","+str(probe2)

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
    done.value = False
    done.value=True

    # pull DONE pin and sleep

else:


    oled.fill(0)
    oled.text("Never got sat fix.",0,0,True)
    oled.show()
    time.sleep(3)
    print ("never got a satellite fix")
    print ("PULL DONE")

    done.value = False
    done.value=True

    # pull DONE pin and sleep