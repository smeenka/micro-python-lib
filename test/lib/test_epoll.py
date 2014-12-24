print("==== /sd/test/lib/test_epoll.py")
import sys
import select
import os
import pyb

# create new usb serial port
usb = pyb.USB_VCP()

# create instance of poll class
ep = select.poll()
# register usb serial port for polling
ep.register(usb, 1)

while True:
    res = ep.poll(2000)
    print(res)
    for ev, fd in res:
        print(os.read(fd, 256))

    if res:
        if usb.any():
            print ("Received:",usb.readall() )
        else:
            print ("Sorry no characters ... ")


    else:
        print ("Empty list received")

