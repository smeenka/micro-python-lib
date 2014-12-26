# lcd.py -- put your code here!

import pyb

lcd = pyb.LCD('X')
lcd.light(True)

def test():
    for x in range(-80, 128):
	lcd.fill(0)
	lcd.text('Hello uPy!', x, 10, 1)
	lcd.show()
	pyb.delay(2000)


test()
