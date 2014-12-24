print("==== /sd/test/lib/test_select.py")

import pyb
import time
import select


lcd = pyb.LCD('X')
lcd.light(True)


usb = pyb.USB_VCP()

poll = select.poll()


x = 0
y = 0
c = 0

def p():
    x = 0
    y = 0
    while True:
        time.sleep(5)
        while usb.any():
            c = usb.read(1)

            print (c)
            lcd.text(c, x, y, 2)
            lcd.show()
            x += 8
            if x > 120:
                x = 0
                y += 10


p()
