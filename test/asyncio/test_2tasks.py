# ------------------------------------------------------------
# pyos.py  -  The Python Cooperative Operating System
#
# ------------------------------------------------------------
print("==== /sd/test/asyncio/test_2tasks.py")

import logging
log = logging.getlogger("test_2tasks")
logs = logging.getlogger("scheduler")
logt = logging.getlogger("task")
logs.setLevel(logging.TRACE)
logt.setLevel(logging.TRACE)
logging.setGlobal(logging.DEBUG)

import time,sys
import asyncio

# Two tasks
def foo():
    fooc = 0
    while fooc < 25:
        log.info ("I'm foo %d",fooc)
        fooc += 1
        yield

def bar():
    barc = 0
    while barc < 25:
        log.info("I'm bar %d",barc)
        barc +=1
        yield
    yield asyncio.KillOs()


# Run them
sched = asyncio.Scheduler()
sched.new(bar(), name = "bartask", period = 700)
sched.new(foo(), name = "footask", period = 500)

sched.mainloop()
