# ------------------------------------------------------------
# pyos.py  -  The Python Cooperative Operating System
#
# ------------------------------------------------------------
print("==== /sd/test/asyncio/test_taskwait.py")

import logging
import pyb
log = logging.getlogger("test_taskwait")
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
    yield
    tid = yield asyncio.GetTid()
    log.info("Task led0() taskid: %d", tid)
    while total < 25:
        leds[0].toggle()
        total += 1
        yield
    log.info("Task led0() finished!")

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
def  wait4task0(tid0):
    yield
    result = yield asyncio.WaitTask(tid0)
    log.info("wait4task0: Waiting for task %d to end.Did I wait? : %s",tid0 ,result)
    yield asyncio.KillOs()

now = pyb.millis()

# Run them
sched = asyncio.Scheduler()
tid0 = sched.new(led0(),  period = 200)
sched.new(led1(),  period = 400, time2run = now +200)
sched.new(led2(),  period = 400, time2run = now +400)
sched.new(wait4task0(tid0)  ,period = 1000,   )

sched.mainloop()
