

import os
import heapq as heapq
from heapq import heapqueue

for name in heapq.heapqueue.__all__:
    print ("heapq.heapqueue: Current object :",name)

for name in heapqueue.__all__:
    print ("heapqueue: Current object :",name)


print("Current dir: %s" % os.getcwd())
h = []
heapq.heappush(h, ("c",10.1, 1))
print(h)
heapq.heappush(h, ("B",10000000.1, 1))
print(h)
heapq.heappush(h, ("B",1.1, 1))
print(h)
heapq.heappush(h, ("A",1.1, 1))
print(h)
heapq.heappush(h, ("Z",1.1, 1))
print(h)

while h:
    print("Pop from queue: " ,heapq.heappop(h) )
    print(h)

#assert h == [(1.1, 1), (10.1, 0),(10.1, 0)]
