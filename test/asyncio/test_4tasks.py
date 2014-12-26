# ------------------------------------------------------------
# pyos.py  -  The Python Cooperative Operating System
#
# ------------------------------------------------------------
print("==== /sd/test/asyncio/test_4tasks.py")

import logging
import pyb
log = logging.getlogger("test_2tasks")
logs = logging.getlogger("scheduler")
logs.setLevel(logging.TRACE)
logging.setGlobal(logging.DEBUG)

import time,sys
import asyncio

leds = []
for i in range(1,5):
    led = pyb.LED( i  )
    led.on()
    leds.append(   led )

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

now = pyb.millis()

# Run them
sched = asyncio.Scheduler()
sched.new(led0(),  period = 1000, time2run = now +2000)
sched.new(led1(),  period = 1000, time2run = now +4200)
sched.new(led2(),  period = 1000, time2run = now +6400)
sched.new(led3(),  period = 1000, time2run = now +8600 )

sched.mainloop()
