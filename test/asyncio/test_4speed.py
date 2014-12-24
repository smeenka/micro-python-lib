# ------------------------------------------------------------
# pyos.py  -  The Python Cooperative Operating System
#
# ------------------------------------------------------------
print("==== /sd/test/asyncio/test_4speed.py")

import logging
log = logging.getlogger("test_4speed")
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

lcd = pyb.LCD('X')

lcd.text('Testing 4speed!', 0, 0, 1)
lcd.show()

# ------------------------------------------------------------
#                      === Example ===
# ------------------------------------------------------------
total = [0,0,0,0]
# 4 tasks
def  led0(total):
    yield
    while True:
        total[0] += 1
#       leds[0].toggle()
        yield

def  led1(total):
    yield
    while True:
        total[0] += 1
        yield
def  led2(total):
    yield
    while True:
        total[0] += 1
        yield
def  led3(total):
    yield
    while True:
        total[0] += 1
        yield
def  led4(total):
    yield
    while True:
        total[0] += 1
        yield
def  led5(total):
    yield
    while True:
        total[0] += 1
        yield


def  evaluate(total, lcd):
    lcd.light(False)
    yield
    starttime = pyb.micros()
    yield
    endtime = pyb.micros()
    t = total[0]
    lcd.light(True)
    us = endtime - starttime

    text = "c/s: %f " % (t/ 10)
    lcd.text(text, 0, 10, 1)
    lcd.show()

    log.info("Total micros in 10 second runtime: %f", us / 1000000)
    log.info("Total counts:  %d counts /sec: %f ", t, t / 10)




now = pyb.millis()
#wait until millis is changing
while pyb.millis() == now:
    pass
now = pyb.millis()


# Run them
sched = asyncio.Scheduler()

startmicro = pyb.micros()
sched.new(led0 ( total )    , time2run = now + 10,  period = 1000)
sched.new(led1  ( total )  , time2run = now + 10, period = 10)
sched.new(led2  ( total )  , time2run = now + 10, period = 10)
sched.new(led3 ( total )   , time2run = now + 10,  period = 1)
sched.new(led4 ( total )   , time2run = now + 10,  period = 1)
sched.new(led5 ( total )   , time2run = now + 10,  period = 1)
sched.new(evaluate( total, lcd  ) ,  time2run = now  + 10, period = 10000)


micros = pyb.micros() - startmicro
log.info("Total amount of micros needed for creating tasks:  %d ", micros)


sched.mainloop()
