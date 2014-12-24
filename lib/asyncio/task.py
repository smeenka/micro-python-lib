# ------------------------------------------------------------
# pyos.py  -  The Python Cooperative Operating System
#
# ------------------------------------------------------------
#                       === Tasks ===
# ------------------------------------------------------------
from  logging import *
log = logging.getlogger("task")

class Task(object):
    taskid = 0
    def __init__(self,target, name = "", prio = 10, period = 0, time2run = 0):
        """ Create task and run its target to the first yield
            Target must be a generator object
        """
        Task.taskid += 1
        self.tid     = Task.taskid   # Task ID
        self.target  = target         #  create coroutine from given generator
        self.params  = None        # Value to send/receive
        self.prio    = prio
        if name == "":
            self.name = "task_%d" % self.tid
        else:
            self.name = name
        self.period   = period       # zero:     run now
                                     # negative: run once
                                     # positive: run at interval
        self.time2run = time2run            # time to run(in millis since boot)
        log.trace("Created task %s %d ", self.name,self.tid)
        self.target.send(None)

    def run(self):
        """ Run a task until it hits the next yield statement """
#        log.trace(" run task %s ", self.name)
        return self.target.send(self.params)

    def __lt__(self,other):
        """ compare other task with this one. If  this task is smaller than the other one, return True else False """
        if self. time2run < other.time2run:
            return True;
        if   self.prio < other.prio:
            if self. time2run == other.time2run:
                return  True
        return False
