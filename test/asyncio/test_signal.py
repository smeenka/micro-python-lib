# ------------------------------------------------------------
# pyos.py  -  The Python Cooperative Operating System
#
# ------------------------------------------------------------
print("==== /sd/test/asyncio/test_signal.py")

import logging
import pyb
log = logging.getlogger("test_signal")
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

# ------------------------------------------------------------
#                      === Example ===
# ------------------------------------------------------------
total = 0


# 4 tasks
def  wait0():
    total = 0
    while True:
        leds[0].toggle()
        total += 1
        yield

def  wait1():
    yield
    while True:
        result =yield asyncio.Wait4Signal("Hello")
        if result == None:
            result = 0x1234
        log.info("Task wait1() got signal value: %d ",result)

def  wait2():
    yield
    while True:
        result =yield asyncio.Wait4Signal("Hello")
        if result == None:
            result = 0x1234
        log.info("Task wait2() got signal value: %d ",result)

def  wait3():
    yield
    while True:
        result =yield asyncio.Wait4Signal("Hello")
        if result == None:
            result = 0x1234
        log.info("Task wait3() got signal value: %d ",result)
        if result == 10:
            yield asyncio.KillOs()

def  sender():
    count = 0
    yield
    while True:
        leds[2].toggle()
        log.info("Sending signal hello, value: %d ", count)
        yield asyncio.SendSignal("Hello", count)
        count += 1

now = pyb.millis()

# Run them
sched = asyncio.Scheduler()
sched.new( wait0() ,period = 100  )
sched.new( wait1()  )
sched.new( wait2()  )
sched.new( wait3()  )
sched.new( sender(), period = 900 )

sched.mainloop()
