import network
import ntptime
import time
from machine import Pin
from servo import SERVO

# --- Paramètres Wi-Fi ---
SSID = "MonWifi"          
PASSWORD = "MonMotDePasse" 

# --- Connexion au Wi-Fi ---
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

print("Connexion au Wi-Fi...")
while not wlan.isconnected():
    time.sleep(0.5)
    print(".", end="")

print("\nConnecté !")

# === Synchronisation de l’heure avec un serveur NTP ===
ntptime.settime()

utc_offset = 1  # Décalage horaire en heures

# === Initialisation du servo sur la broche GP18 ===
servo = SERVO(Pin(18))

# === Fonction d'interruption sur le bouton ===
def change_timezone(pin):
    global utc_offset, last_press
    utc_offset += 1
    
    if utc_offset > 12:
        utc_offset = -12
    print("\nFuseau horaire changé :", "UTC{:+d}".format(utc_offset))

# === Bouton sur GP16 avec interruption ===
button = Pin(16, Pin.IN, Pin.PULL_UP)
button.irq(trigger=Pin.IRQ_FALLING, handler=change_timezone)

print("Fuseau horaire initial : UTC{:+d}".format(utc_offset))

# === Boucle principale ===
while True:
    t = time.localtime(time.time() + utc_offset * 3600)
    hour, minute, sec = t[3], t[4], t[5]

    # Conversion heure en angle (24 h = 180°)
    angle = (hour + minute / 60) * (180 / 24)
    servo.turn(angle)

    print("UTC{:+d} | {:02d}:{:02d}:{:02d}, angle = {:.1f}°".format(
        utc_offset, hour, minute, sec, angle))
    time.sleep(1)

