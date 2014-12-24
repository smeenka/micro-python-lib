# main.py -- put your code here!
print("==== /sd/main.py")

import pyb
import os

blue = pyb.LED(4)
blue.intensity(10)

red = pyb.LED(1)
red.on()

os.chdir('/sd/test/asyncio')
#os.chdir('/sd/test/lib')
import test
