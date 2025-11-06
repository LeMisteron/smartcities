from ws2812 import WS2812
from machine import Pin, ADC
from utime import sleep, ticks_ms, ticks_diff
import urandom

# --- Initialisation ---
led = WS2812(18, 1)           # LED RGB sur D18
mic = ADC(1)                  # Microphone sur ADC1

# --- Paramètres ---
seuil = 55                    # Seuil de détection
delai_min = 150               # Délai min entre deux battements (ms)
duree_moyenne = 60000         # Durée d’une minute en ms

# --- Variables de mesure ---
temps_dernier_battement = 0
dernier_calcul = 0
bpm_mesures = []              # Stocke les BPM instantanés sur 1 minute

# --- Fonction utilitaire ---
def couleur_aleatoire():
    return (urandom.getrandbits(8), urandom.getrandbits(8), urandom.getrandbits(8))

# --- Boucle principale ---
while True:
    valeur = mic.read_u16() / 256  # Normalisation 0–255
    maintenant = ticks_ms()

    # Détection du battement
    if valeur > seuil and (ticks_diff(maintenant, temps_dernier_battement) > delai_min):
        if temps_dernier_battement != 0:
            intervalle = ticks_diff(maintenant, temps_dernier_battement)
            bpm = 60000 / intervalle
            bpm_mesures.append(bpm)
            print("BPM instantané :", int(bpm))

        # Mise à jour du temps du dernier battement
        temps_dernier_battement = maintenant

        # Effet LED
        couleur = couleur_aleatoire()
        led.pixels_fill(couleur)
        led.pixels_show()

    # Toutes les 60 secondes → calcul et enregistrement moyenne BPM
    if ticks_diff(maintenant, dernier_calcul) >= duree_moyenne:
        if bpm_mesures:
            moyenne_bpm = sum(bpm_mesures) / len(bpm_mesures)
            print("---- Moyenne sur 1 minute :", int(moyenne_bpm), "BPM ----")

            try:
                with open("bpm_log.txt", "a") as f:
                    f.write(f"{int(moyenne_bpm)}\n")
            except Exception as e:
                print("Erreur écriture fichier :", e)

            bpm_mesures.clear() # nouvelle valeur à stocker

        dernier_calcul = maintenant

    sleep(0.02)
