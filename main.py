# Afficheur V5.0
# Dernière mise à jour : 17/03/2025
# Etat : ....................... En cours
# Test hardware : .............. ok le 17-03-2025 
# Capteur de luminsoité : ...... En cours
# Bus I2C : .................... ok
#  : ................... ok
#  : .............. ok
#  : ................................ ok
#  : ........................... ok
#  : ..................... ok
#  : ..................... ok
#  : ................... ok
version = "16-05-2025" 

import network
import math
import espnow
import time
import machine
from afficheur import Afficheur7Segments
from machine import I2C, Pin, reset
#from animations import *

# Adresse MAC de la carte
#b'\xb4\x8a\n\x8a/\x9c'

oldValue = 0
oldLum = 0
oldColor = 0

# Messages reçus sour la forme d'une chaine de caractère
# CouleurJ1 CouleurJ2 Luminosité J1S1 J1S2 J1S3 J2S1 J2S2 J2S3
# 0 - 7     0 - 7     1 - 3      0 - 7 

# Adresse MAC du pupitre
emetteur = b'\xb4\x8a\n\x8a0`'

# Bus I2C pour capteur de luminosité
i2c = I2C(0, scl=Pin(22), sda =Pin(21) , freq=400000) 

def luxsensor():
    clear_lsb = 0 #def variables de lecture du capteur
    clear_msb = 0
    try:
        reading = i2c.readfrom(72,2)
        clear_lsb = reading[1]
        clear_msb = reading[0]
        clear = (clear_msb << 6) + (clear_lsb >> 2) # Decalage des bits
        ambLux = int(clear *(-100/1023) + 100) # Equation affine ajustement valeur mesurée
    except:
        ambLux=oldLux
    return ambLux

# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)
sta.active(True)
print(sta.config('mac'))

e = espnow.ESPNow()
#e.add_peer(emetteur)
e.active(True)

segment_pins = [33, 27, 26, 14, 13, 5, 16]
afficheur = Afficheur7Segments(segment_pins)

afficheur.afficheur_off()

# Attente de connexion du pupitre au démarrage
# Wave rouge vert bleu en boucle
while None in e.recv(100):
    afficheur.wavesymbol("8","red",80)
    afficheur.wavesymbol("8","green",80)
    afficheur.wavesymbol("8","blue",80)

host='0'
oldMsg="Rien"
    
print ("Afficheur V5.0 - " + version)

lum = userLum = 3

while True:
    # Essai en cas de données incohérentes
    test = e.recv(100)
    if None not in test :
        print(test)
        host, msg = test
        msg = msg.decode("utf-8")
        if msg != oldMsg:
            if msg is "U":
                f = open("update.txt", "w")
                f.write("True")
                f.close()
                # Afficher U pour update en cours !
                afficheur.afficheur_set("U","red",30)
                machine.reset()
            oldMsg = msg
            msgSplit = msg.split("-")
            print(msgSplit)
            color = msgSplit[0]
            if color not in afficheur.couleurs_rgb:
                color=oldColor
            value = msgSplit[1]
            userLum = msgSplit[2]
            if value != oldValue or color != oldColor or userLum != oldUserLum:
                lum = (int(userLum) * 100)/3
                afficheur.afficheur_set(value,color,lum)
            oldValue = value
            oldUserLum = userLum
            oldColor = color