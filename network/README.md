Ce code connecte un Raspberry Pi Pico W à un réseau Wi-Fi en utilisant la bibliothèque network de MicroPython.
Il récupère ensuite l’heure exacte depuis un serveur NTP via la bibliothèque ntptime, puis ajuste cette heure selon un décalage horaire (variable utc_offset).

Un servo-moteur, contrôlé par la classe SERVO (bibliothèque servo), tourne proportionnellement à l’heure courante : 0° correspond à minuit et 180° à 24h.

Un bouton déclenche une interruption à chaque appui pour changer de fuseau horaire (de -12 à +12).

