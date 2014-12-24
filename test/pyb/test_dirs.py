
import sys
import os

print(os.getcwd())

l = os.listdir()
print(l)
assert "test_dirs.py" in l

for t in os.walk("."):
    print(t)

for t in os.walk(".", False):
    print(t)
