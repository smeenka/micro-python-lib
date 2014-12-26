print("==== /sd/test/lib/test_select.py")

import pyb
import time
import select


lcd = pyb.LCD('X')
lcd.light(True)





x = 0
y = 0
c = 0

def p():
    usb = pyb.USB_VCP()
    x = 0
    y = 0
    rlist = []
    wlist = []
    xlist = []
    while True:
        #rlist = [usb]          # will fail  TypeError: object with stream.ioctl required
        select.select ( rlist, wlist, xlist, 1)
        print ("rlist: ", rlist)

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
