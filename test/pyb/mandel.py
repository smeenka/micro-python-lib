print("==== /sd/test/lib/mandel.py")
import pyb

def mandelbrot():
    # returns True if c, complex, is in the Mandelbrot set

    def in_set(c):
        z = 0
        for i in range(40):
            z = z*z + c
            if abs(z) > 60:
                return False
        return True

    lcd.fill(0)                 # clear the buffer
    for u in range(140):
        for v in range(32):
            if in_set((u / 32 - 2) + (v / 16 - 1) * 1j):
                lcd.pixel(u, v,1)
        lcd.show()

# PC testing
print("==== This test needs lcd connected")
lcd = pyb.LCD('X')
lcd.light(True)

mandelbrot()
lcd.text('Hello!', 80, 0, 1)
lcd.text('uPy!  ', 90, 20, 1)
lcd.show()

