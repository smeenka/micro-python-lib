micro-python-lib
================

Thank you for the great work you have done Damien George!

Really appreciate your work done.

Goal for this repository is:
* work on micro python libraries
* work on the PyOs, cooperative multitasking os
* creating tests for the libraries
* creating a way of working with micro python 

How to use this repository
* copy all files onto a micro sd card
* insert sd card into you micro python board and reboot
* Select directory in main.py, and select test to run in /sd/test/subdir/test/.py


About asyncio:
* rewrote this library after following the Curious Course on Coroutines and Concurrency course at http://www.dabeaz.com/coroutines/
* each coroutine is wrapped in a tasks, to make it more easy to schedule repetative task
* see the /sd/test/asyncio direcory for how to use this library

To do: 
* the usb serial port does not work with the select lib. So for usb serial I created a workaround
* not tested the select lib and polling task, because I do not have a tcp-ip cc3300 module yet 
* At the moment no task is ready the micro should  sleep 




