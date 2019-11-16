https://learn.adafruit.com/circuitpython-essentials/circuitpython-uart-serial




>>> import satbroad
b'AT\r\r\nOK\r\n'
b'AT&K0\r\r\nOK\r\n'
b'AT+SBDWT=Hello Somerville\r\r\nOK\r\n'
b'AT+SBDIX\r'
None
None
None
b'\r\n+SBDIX: 32, 11, 2, 0, 0, 0\r\n\r\n'
b'OK\r\n\x00'
None
None
None
None
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "satbroad.py", line 39, in <module>
KeyboardInterrupt: 

---

cr1220

---

getting the GPS data:
https://learn.adafruit.com/adafruit-ultimate-gps/direct-computer-wiring

ssd1306:
https://learn.adafruit.com/micropython-hardware-ssd1306-oled-display/circuitpython


getting the text:

>>> import board
>>> import busio as io
>>> i2c = io.I2C(board.SCL, board.SDA)
>>> import adafruit_ssd1306
>>> oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
>>> oled.text('hello',0,0,True)
>>> oled.show()
>>> 

boost has quiescent of 1 mA