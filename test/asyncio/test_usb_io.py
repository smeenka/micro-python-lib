# ------------------------------------------------------------
# pyos.py  -  The Python Cooperative Operating System
#
# ------------------------------------------------------------
print("==== /sd/test/asyncio/test_usb_io.py")


import logging
import pyb
log = logging.getlogger("test_usb_io")
logs = logging.getlogger("scheduler")
logt = logging.getlogger("task")
logs.setLevel(logging.TRACE)
logt.setLevel(logging.TRACE)
logging.setGlobal(logging.DEBUG)

import time,sys
import asyncio

leds = []
for i in range(1,5):
    led = pyb.LED( i  )
    led.on()
    leds.append(   led )

# create new usb serial port
usb = pyb.USB_VCP()

# ------------------------------------------------------------
#                      === Example ===
# ------------------------------------------------------------
total = 0
# 4 tasks
def  led0():
    total = 0
    while True:
        leds[0].toggle()
        total += 1
        yield
def  led1():
    total = 0
    while True:
        leds[1].toggle()
        total += 1
        yield
def  led2():
    total = 0
    while True:
        leds[2].toggle()
        total += 1
        yield
def  led3():
    total = 0
    while True:
        leds[3].toggle()
        total += 1
        yield

def  usbIO():
    yield
    buffer = bytearray([0])
    while True:
        yield asyncio.IOWait("usb")
        line = ""
        while usb.any():
            usb.recv(buffer)
            line = "%s%c"%(line,buffer[0])
        log.info("Received: %s ", line )


now = pyb.millis()

sched = asyncio.Scheduler()
sched.new(led0(),  period = 1000, time2run = now +2000)
sched.new(led1(),  period = 1000, time2run = now +4200)
sched.new(led2(),  period = 1000, time2run = now +6400)
sched.new(led3(),  period = 1000, time2run = now +8600 )
sched.new(usbIO() )

#register usb for IO polling at the scheduler
sched.registerUsb(usb)

# Run them
sched.mainloop()
