# ------------------------------------------------------------
# pyos.py  -  The Python Cooperative Operating System
#
# ------------------------------------------------------------
#                      === Scheduler ===
# ------------------------------------------------------------
import logging
from .task import Task
from .system_calls import *
import pyb
import select

log = logging.getlogger("scheduler")


class Scheduler(object):
    def __init__(self):
        self.ready   = []
        self.taskmap = {}
        self.taskStartTime = 0

        # Tasks waiting for other tasks to exit
        self.exit_waiting = {}
        self.signal_waiting = {}

        # I/O waiting
        self.io_waiting  = {}
        self.poll = select.poll()   # create instance of poll class
        self.usb = None


    def new(self,target,name = "", prio = 10, period = 0, time2run = 0):
        """ Create new task from target. Return taskid form new task
            Target must be of type generator, prio 1 is higgest prio,
            period is time in ms, timer2run is starttime in ms
        """
        newtask = Task(target,name,prio,period, time2run)
        self.taskmap[newtask.tid] = newtask
        self.schedule(newtask)
        return newtask.tid

    def exit(self,task):
        log.trace("Task %d terminated" , task.tid)
        del self.taskmap[task.tid]
        # pop waiting list for this task (or empty list if none is waiting)
        waiting = self.exit_waiting.pop(task.tid,[])
        for task in waiting:
            self.schedule(task)

    def waitforexit(self,task,waittid):
        if waittid in self.taskmap:
            self.exit_waiting.setdefault(waittid,[]).append(task)
            return True
        else:
            return False

    def wait4signal(self, task, signal):
        self.signal_waiting.setdefault(signal,[]).append(task)

    def sendsignal(self,signal,value):
        # pop waiting list for this signal (or empty listt if none is waiting)
        log.info ("sendsignal  %s , %d " ,signal ,value)
        waiting = self.signal_waiting.pop(signal,[])
        for task in waiting:
            task.params = value
            self.schedule(task)

    # I/O waiting
    def registerUsb(self,usb):
        self.usb = usb

    def registerStream(self,fd, readwrite):
        self.poll.register(fd,readwrite)

    def iowait(self,fd,task):
        self.io_waiting[fd] = task

    def _pollingCoroutine(self):
        while True:
            yield
            readylist= self.poll.poll(0)
            readylist= []
            for fd in readylist:
                readyTask = self.io_waiting.pop(fd,None)
                if readyTask:
                    self.schedule(readyTask)

            if self.usb and self.usb.any():
                readyTask = self.io_waiting.pop("usb",None)
                if readyTask:
                    self.schedule(readyTask)

    def schedule(self,task):
        self.ready.append(task)
        self.readySiftDown()

    def mainloop(self):
        pollingTask = Task(self._pollingCoroutine(), name = "IOPoller",period = 1000)
        self.schedule(pollingTask)

        while True:
            if self.ready:
                # fix current millis, before start of task
                taskStartTime = pyb.millis()
                task = self.ready[0]     # peek queue
                if task.time2run <= taskStartTime:

                    self.ready.pop( 0 )  # remove item for queue
#                    rq = "queue: "
#                    for t in self.ready:
#                        rq = "%s %s %d" % (rq,t.name,t.tid)
#                    log.info (rq)

                    #log.trace ("Running task %s , %d " ,task.name ,task.tid)
                    try:
                        result = task.run()
                    except StopIteration:
                        self.exit(task)
                        continue  # do not reschedule current task

                    if result:
                        if isinstance(result, IOWait):
                             self.iowait(result.fd,task)
                             continue  # do not reschedule current task

                        if isinstance(result, SendSignal):
                             self.sendsignal(result.signal,result.value)
                             # reschedule current task

                        if isinstance(result, Wait4Signal):
                             self.wait4signal(task,result.signal)
                             continue  # do not reschedule current task

                        if isinstance(result, GetTaskRef):
                             task.params  = task
                             # reschedule current task

                        if isinstance(result, GetTid):
                             task.params  = task.tid
                             # reschedule current task

                        if isinstance(result, WaitTask):
                             result = self.waitforexit(task,result.tid)
                             task.params  = result
                             # If waiting for a non-existent task,
                             # reschedule current task now
                             if  result:
                                 continue

                        if isinstance(result, NewTask):
                             log.trace(  "SystemCall NewTask called by: ", task.name)
                             tid = self.sched.new(result.target, result.name,result.prio,result.time2run)
                             task.params  = tid
                             # reschedule current task

                    task.time2run = task.period + taskStartTime
                    self.ready.append(task)
                    self.readySiftDown()
                else:
                    pass
            else:
                pass



    """ priority queue invariant quard
    Prioriy queue is a queue for which a[k] < a[k+1]  for all k
    Popping the first element from the queue will maintian this invariant.
    When pushing an element at the end of the array, the invariant must be guarded.
    This is done by comparing each 2 elements and swapping element if needed
    """
    def  readySiftDown(self):
        heap = self.ready
        hlen = len(heap)

        if hlen < 2:
            return

        posLeft = hlen  - 2
        # Follow the path to the root, shifting 2 neigbours if in wrong order
        # Stop at the monent no shift is needed
        # newtask fits.
        while posLeft >= 0 :
            posRight = posLeft + 1
            left  = heap[posLeft]
            right =heap[posRight]
            if  right.__lt__( left):
                heap[posLeft]   = right
                heap[posRight] = left
            else:
                break
            posLeft = posLeft - 1




