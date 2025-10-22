from machine import Pin, I2C, ADC, PWM
from time import sleep
import dht
from lcd1602 import LCD1602

# --- Capteur DHT11 ---
sensor = dht.DHT11(Pin(20))

# --- Potentiomètre ---
#définit la température de consigne
pot = ADC(0)

# --- LED ---
led = Pin(18, Pin.OUT)

# --- Buzzer ---
buzzer = PWM(Pin(14))
buzzer.duty_u16(0) 

# --- Afficheur LCD I2C---
i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=400000)
lcd = LCD1602(i2c, 2, 16)
lcd.clear()


# === FONCTION POUR LIRE LE POT ===
def map_temp(adc_value):
    return 15 + (adc_value / 65535) * (35 - 15)#renvoie une valeur entre 15°C et 35°C pour température de consigne

# === BOUCLE PRINCIPALE ===
while True:
        # Lecture du capteur DHT11 (valeur en °C)
        sensor.measure()
        temp = sensor.temperature()

        # Lecture du potentiomètre, température de consigne
        pot_val = pot.read_u16()
        temp_set = int(map_temp(pot_val))

        # Affichage des valeurs sur LCD
        lcd.setCursor(0, 0)
        lcd.print(f"SET:{temp_set:2d}C   ")
        lcd.setCursor(0, 1)
        lcd.print(f"AMBIENT:{temp:2d}C   ")

        # --- Gestion des alertes ---
        if temp > temp_set + 3:
            # Surchauffe → clignotement rapide + alerte sonore
            led.value(1)
            buzzer.freq(440)
            buzzer.duty_u16(32768)  # 50% rapport cyclique
            sleep(0.5)
            led.value(0)
            buzzer.duty_u16(0)
            sleep(0.5)

        elif temp > temp_set:
            # Température légèrement supérieure, clignotement lent
            led.value(1)
            buzzer.duty_u16(0)
            sleep(1)
            led.value(0)
            sleep(1)

        else:
            # Température sous contrôle, LED et buzzer désactivés
            led.value(0)
            buzzer.duty_u16(0)
            sleep(1.5)

