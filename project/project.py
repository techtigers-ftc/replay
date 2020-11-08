import machine, neopixel
from machine import Pin
import time
np = neopixel.NeoPixel(machine.Pin(5), 1, bpp=4)

np[0] = (200, 0, 0, 0)
np.write()
time.sleep(2)

p2 = Pin(4, Pin.IN)

light_on = False

def on():
    np[0] = (200, 0, 0, 0)
    np.write()

def off():
    np[0] = (0,0,0,0)
    np.write()

while True:
    pressed = p2.value()
    if pressed == 0:
        print("Pressed")
        on()
    else:
        off()
    print(p2.value())
    time.sleep(.2)
        


