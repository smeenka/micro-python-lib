print("==== /sd/test/lib/test_dirs.py")
import sys
import os

print(os.getcwd())

l = os.listdir()
print(l)
assert "test_dirs.py" in l

