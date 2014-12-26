print("==== /sd/test/lib/timer.py")
import pyb

tim4 = pyb.Timer(4)              # create a timer object using timer 4
tim4.init(freq=2)                # trigger at 2Hz
tim4.callback(lambda t:pyb.LED(1).toggle())

def timer_tick(t):
    pyb.LED(4).toggle()



tim6 = pyb.Timer(6, freq=1)    # freq in Hz
tim6.callback(timer_tick)     # set callback for update interrupt (t=tim


tim7 = pyb.Timer(7)              # create a timer object using timer 4
tim7.init(freq=10)                # trigger at 10Hz
tim7.callback(lambda t:pyb.LED(2).toggle())

tim8 = pyb.Timer(8)              # create a timer object using timer 8
tim8.init(freq=3)                # trigger at 3Hz
tim8.callback(lambda t:pyb.LED(3).toggle())

print("==== timer ok")
