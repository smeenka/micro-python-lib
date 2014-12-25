# ------------------------------------------------------------
# pyos.py  -  The Python Cooperative Operating System
#
# ------------------------------------------------------------
print("==== /sd/test/asyncio/test_gettaskref.py")

import logging
log = logging.getlogger("test_taskref")
logs = logging.getlogger("scheduler")
logt = logging.getlogger("task")
logs.setLevel(logging.TRACE)
logt.setLevel(logging.TRACE)

logging.setGlobal(logging.DEBUG)

import pyb
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
    sos = [(1,1),(1,1),(1,1),   (2,1),(2,1),(2,1),    (1,1),(1,1),(1,10) ]
    yield
    task =  yield asyncio.GetTaskRef()
    log.info ("My task name (of generator led0 is: %s", task.name)
    total = 0
    while True:
        # pick next signal pair
        signal = sos.pop(0)
        sos.append(signal)

        task.period =signal[0] * 100
        leds[0].on()
        yield

        task.period =signal[1] * 100
        leds[0].off()
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
        if total > 10:
            asyncio.KillOs()


now = pyb.millis()

# Run them
sched = asyncio.Scheduler()
sched.new(led0(),  period = 1000, time2run = now +000)
sched.new(led1(),  period = 1000, time2run = now +4200)
sched.new(led2(),  period = 1000, time2run = now +6400)
sched.new(led3(),  period = 1000, time2run = now +8600 )

log.info("test_taskref")
sched.mainloop()
