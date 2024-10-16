import network
import espnow
import time
import machine
from machine import I2C, Pin, reset
from afficheur import *
from animations import *

# Adresse MAC de la carte
#b'\xb4\x8a\n\x8a/\x9c'
# Role de l'afficheur dans le système

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

# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)
sta.active(True)
print(sta.config('mac'))

e = espnow.ESPNow()
#e.add_peer(emetteur)
e.active(True)

while None in e.recv(100): 
    wavesymbol("8","red")
    wavesymbol("8","green")
    wavesymbol("8","blue")

host='0'
oldMsg="Rien"

def luxmeter():
    clear_lsb = 0 #def variables de lecture du capteur
    clear_msb = 0
    try:
        reading = [clear_lsb , clear_msb]
        reading = i2c.readfrom(72,2)
        clear_lsb = reading[1]
        clear_msb = reading[0]
        clear = (clear_msb << 6) + (clear_lsb >> 2) # Decalage des bits
        lux = clear * 1 + 0 # Equation affine ajustement valeur mesurée
        #print ("clear", clear)
    except:
        lux=oldLux
    return lux

def luminosite_auto():
    luxmeter()
    lum = (userLum/3) * luxmeter()
    afficheur_set(oldValue,oldColor,lum)
    
print ("Afficheur V1.0 - 27-08-2024")

lux = oldLux = 0

while True:
    test = e.recv(100)
    #luminosite_auto()
    # Essai en cas de données incohérentes
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
                afficheur_set("U","red",30)
                machine.reset()
            oldMsg = msg
            msgSplit = msg.split("-")
            print(msgSplit)
            color = msgSplit[0]
            if color not in couleurs:
                color=oldColor
            value = msgSplit[1]
            userLum = msgSplit[2]
            if value != oldValue or color != oldColor or userLum != oldUserLum:
                #lum = (userLum/3) * luxmeter()
                lum = userLum
                afficheur_set(value,color,lum)
            oldValue = value
            oldUserLum = userLum
            oldColor = color
