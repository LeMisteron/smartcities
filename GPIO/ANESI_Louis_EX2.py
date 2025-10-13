from machine import Pin, PWM, ADC
from time import sleep

buzzer = PWM(Pin(27))
pot = ADC(0)
led = Pin(18, Pin.OUT)

melodie1 = [1046, 1175, 1318, 1397, 1568, 1760, 1967, 2092]  # mélodies à jouer 
melodie2 = [1568, 1568, 1318, 1568, 2092, 1967]              
melodie_active = 1

def switch_melodie(pin):
    global melodie_active
    melodie_active = 2 if melodie_active == 1 else 1

button = Pin(16, Pin.IN, Pin.PULL_DOWN)
button.irq(trigger=Pin.IRQ_RISING, handler=switch_melodie)  # front montant


while True:
    # Sélection de la mélodie à jouer
    if melodie_active == 1: 
            notes = melodie1 
    else: 
        notes = melodie2

    # Lecture de la mélodie sélectionnée
    for freq in notes:
        buzzer.freq(freq)

        # Clignotement LED et modification du volume en temps réel
        for i in range(30):  # 30 x 10 ms = 0,3 s par note
            pot_value = pot.read_u16()
            volume = int((pot_value / 65535) * 2000) #limite le volume pour une meilleur audition
            buzzer.duty_u16(volume)

            if i % 15 == 0: # la led clignote en rythme avec la mélodie
                led.toggle()

            sleep(0.01)

    buzzer.duty_u16(0)
    led.off()  # éteindre la led entre les mélodies
    sleep(0.5)
