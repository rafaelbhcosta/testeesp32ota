from machine import TouchPad, Pin
from time import sleep

tot = TouchPad(Pin(4))

while True:
    print(tot.value())