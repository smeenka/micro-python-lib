print("==== /sd/test/lib/test_poll.py")
import sys
import select
import os
import pyb

"""
Note that this test will fail:
==== /sd/test/lib/test_poll.py
Traceback (most recent call last):
  File "main.py", line 16, in <module>
  File "test.py", line 5, in <module>
  File "test_poll.py", line 13, in <module>
TypeError: object with stream.ioctl required
"""

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

