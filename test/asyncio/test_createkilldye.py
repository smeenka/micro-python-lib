# ------------------------------------------------------------
# pyos.py  -  The Python Cooperative Operating System
#
# ------------------------------------------------------------
print("==== /sd/test/asyncio/test_createkilldye.py")

import logging
log = logging.getlogger("test_createkilldye")
logs = logging.getlogger("scheduler")
logs.setLevel(logging.TRACE)
logging.setGlobal(logging.DEBUG)

import pyb
import time,sys
import asyncio

leds = []
for i in range(1,5):
    led = pyb.LED( i  )
    led.on()
    leds.append( led )

# ------------------------------------------------------------
#                      === Example ===
# ------------------------------------------------------------
total = 0
# 4 tasks

def  led0():
    log.info("Task led0 created!")
    while True:
        leds[0].toggle()
        yield
    log.info("Task led0 dies!")

def  led1():
    while True:
        leds[1].toggle()
        yield
    log.info("Task led1 dies!")

def  led2():
    while True:
        leds[2].toggle()
        yield
    log.info("Task led2 dies!")

def  led3():
    while True:
        leds[3].toggle()
        yield
    log.info("Task led3 dies!")


def  master_of_universe():
    tid = 0
    leds[3].off()
    leds[0].off()
    yield
    log.info("Creating task led0. Red led goes flashing fast!")
    tid = yield  asyncio.CreateTask( led0(),  period = 100, prio = 11  )

    log.info("Kill  task led0 with tid %d. Red led stops flashing!",tid)
    yield asyncio.KillTask(tid)

    log.info("Kill the os itself!")
    yield asyncio.KillOs()

    log.info("Task master_of_universe is ready!")





now = pyb.millis()

# Run them
sched = asyncio.Scheduler()
sched.new(led0(),  period = 1000,  time2run = now +100)
sched.new(led1(),  period = 300,  time2run = now +100)
sched.new(led2(),  period = 700, time2run = now +200)
sched.new(led3(),                period = 4000, time2run = now +4000)
sched.new(master_of_universe(),  period = 4000, time2run = now +4000 )

log.info("test creating killing tasks")
sched.mainloop()
