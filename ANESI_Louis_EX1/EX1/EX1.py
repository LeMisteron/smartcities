import machine
import utime

button = machine.Pin(18, machine.Pin.IN, machine.Pin.PULL_DOWN)  
led = machine.Pin(16, machine.Pin.OUT)

# Variables de gestion
mode = 0    
last_time = utime.ticks_ms()

while True:
    state = button.value()
    if state == 1:  
        if utime.ticks_diff(utime.ticks_ms(), last_time) > 200:
            mode = (mode + 1) % 3   # cycle entre 0,1,2
            last_time = utime.ticks_ms()
    
    if mode == 0:
        led.value(0)  # éteint
        utime.sleep(0.1)

    elif mode == 1:
        led.toggle()         # clignotement lent
        utime.sleep(1)       

    elif mode == 2:
        led.toggle()         # clignotement rapide
        utime.sleep(0.25)    

