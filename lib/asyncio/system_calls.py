# ------------------------------------------------------------
# pyos.py  -  The Python Cooperative Operating System
#
# ------------------------------------------------------------
#                   === System Calls ===
# ------------------------------------------------------------
import logging
import pyb

log = logging.getlogger("system_call")
log.setLevel(logging.DEBUG)

class SystemCall(object):
    pass

# Return a task its own ID number
class GetTid(SystemCall):
    pass
# Return a task its own task reference
class GetTaskRef(SystemCall):
    pass


# Create a new task, calling coroutine gets a tid of the created task
class NewTask(SystemCall):
    def __init__(self,target, name = "", prio = 10, period = 0, time2run = 0):
        self.target = target
        self.name = name
        self.prio = prio
        self.time2run = time2run


# Kill a task
class KillTask(SystemCall):
    def __init__(self,tid):
        self.tid = tid
    def handle(self):
        task = self.sched.taskmap.pop(self.tid,None)
        if task:
            task.target.close()
            self.task.params  = True
        else:
            self.task.params  = False
        self.sched.schedule(self.task)

# Wait for a task to exit
class WaitTask(SystemCall):
    def __init__(self,tid):
        self.tid = tid


# Wait for reading
class IOWait(SystemCall):
    def __init__(self,fd):
        self.fd = fd
    def handle(self):
        self.sched.iowait(self.fd,self.task)

# Wait for a signal
class Wait4Signal(SystemCall):
    def __init__(self,signal):
        self.signal = signal


class SendSignal(SystemCall):
    def __init__(self,signal,value = None):
        self.signal = signal
        self.value = value



