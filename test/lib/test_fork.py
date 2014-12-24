import sys
sys.path.append("/data/workspace/micro-python/lib")


import os
import time

r, w = os.pipe()
print(r, w)

pid = os.fork()
print("hello", pid)

if not pid:
    i = 0
    print("Child pidpid:", pid)
    print("Child pid:", os.getpid() )
    os.close(r)
    time.sleep(2)
    while True:
        time.sleep(10)
        os.write(w, "from child greetings %d" % i)
        i += 1
    os._exit(0)
else:
    print("Parent pidpid:", pid)
    print("Parent pid:", os.getpid())
    os.close(w)
    while True:
        print(os.read(r, 100))
    print(os.waitpid(pid, 0))
