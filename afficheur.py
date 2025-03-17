# Afficheur V5.0
# Date de création : 11/07/2024
# Etat : En cours de rédaction
# New : Chaque segment est commandé par une sortie indépendante
# Informations :
# Changement des sorties en fonction de la led choisie : ... ok
# Fonctions : led_on / led_off : ........................... ok
# Fonctions : segment_on / segment_off : ................... ok
# Fonctions : afficheur_set / afficheur_off : .............. ok
# Test hardware afficheur : ................................ ok
# Fonctions : raw_on / raw_off : ........................... ok
# Fonctions : column_on / column_off : ..................... ok
# Fonctions : diag45_on / diag45_off : ..................... ok
# Fonctions : diag270_on / diag270_off : ................... ok

from machine import Pin
from neopixel import NeoPixel
from time import sleep
from time import sleep_ms
from machine import I2C, Pin

global nombreTotalLeds
global segmentsAfficheur
global ledsSegment
global luminosity

# Définition de la configuration de l'afficheur
nombreLedsAfficheur = 56
nombreLedsPoints = 0
nombreTotalLeds = nombreLedsAfficheur + nombreLedsPoints #Nombre de leds
segmentsAfficheur = 7 #Nombre de segment de l'afficheur
segmentLeds=[8,8,8,8,8,8,8] #Nombre de leds par segment

# Cablage afficheur
# Segment A : 33 - Segment B : 27 - Segment C : 26 - Segment D : 14
# Segment E : 13 - Segment F : 5 - Segment G : 16 - Points : D7
#pinWemos=[D4,D3,D2,D1,D7,D5,D8]
sgA = NeoPixel(Pin(33, Pin.OUT), 8)
sgB = NeoPixel(Pin(27, Pin.OUT), 8)
sgC = NeoPixel(Pin(26, Pin.OUT), 8)
sgD = NeoPixel(Pin(14, Pin.OUT), 8)
sgE = NeoPixel(Pin(13, Pin.OUT), 8)
sgF = NeoPixel(Pin(5, Pin.OUT), 8)
sgG = NeoPixel(Pin(16, Pin.OUT), 8)

couleurs = ["red","green","blue","cyan","purple","yellow","orange","pink"]
def led_on(number,color,luminosity): #allumer la led pointée avec la couleur
    #Palette de couleurs
    number=number-1
    if number>nombreTotalLeds:
        number=nombreTotalLeds
    if number<=0:
        number=0;
    # Pour le moment on n'utilise pas le capteur de luminosité
    if luminosity > 100:
        luminosity = 100
    if luminosity < 0:
        luminosity = 0
    if color=="blue":
        rgv=[0,0,255]
    elif color=="red":
        rgv=[255,0,0]
    elif color=="green":
        rgv=[0,255,0]
    elif color=="pink":
        rgv=[255,0,255]
    elif color=="yellow":
        rgv=[255,120,0]
    elif color=="cyan":
        rgv=[0,255,255]
    elif color=="purple":
        rgv=[160,32,240]
    elif color=="orange":
        rgv=[255,165,0]
    else :
        rgv=[255,0,0] #rouge par defaut  

    if number>=0 and number<8:
        sgA[number] = (int(rgv[0]*luminosity/100), int(rgv[1]*luminosity/100), int(rgv[2]*luminosity/100))
        sgA.write()           
    if number>=8 and number<16:
        number=number-8
        sgB[number] = (int(rgv[0]*luminosity/100), int(rgv[1]*luminosity/100), int(rgv[2]*luminosity/100))
        sgB.write()
    if number>=16 and number<24:
        number=number-16
        sgC[number] = (int(rgv[0]*luminosity/100), int(rgv[1]*luminosity/100), int(rgv[2]*luminosity/100))
        sgC.write()
    if number>=24 and number<32:
        number=number-24
        sgD[number] = (int(rgv[0]*luminosity/100), int(rgv[1]*luminosity/100), int(rgv[2]*luminosity/100))
        sgD.write()
    if number>=32 and number<40:
        number=number-32
        sgE[number] = (int(rgv[0]*luminosity/100), int(rgv[1]*luminosity/100), int(rgv[2]*luminosity/100))
        sgE.write()
    if number>=40 and number<48:
        number=number-40
        sgF[number] = (int(rgv[0]*luminosity/100), int(rgv[1]*luminosity/100), int(rgv[2]*luminosity/100))
        sgF.write()
    if number>=48 and number<56:
        number=number-48
        sgG[number] = (int(rgv[0]*luminosity/100), int(rgv[1]*luminosity/100), int(rgv[2]*luminosity/100))
        sgG.write()

def led_off(number): #éteindre la led pointée
    number=number-1
    if number>nombreTotalLeds:
        number=nombreTotalLeds
    if number<=0:
        number=0
    if number>=0 and number<8:
        sgA[number] = (0,0,0)
        sgA.write()           
    if number>=8 and number<16:
        number=number-8
        sgB[number] = (0,0,0)
        sgB.write()
    if number>=16 and number<24:
        number=number-16
        sgC[number] = (0,0,0)
        sgC.write()
    if number>=24 and number<32:
        number=number-24
        sgD[number] = (0,0,0)
        sgD.write()
    if number>=32 and number<40:
        number=number-32
        sgE[number] = (0,0,0)
        sgE.write()
    if number>=40 and number<48:
        number=number-40
        sgF[number] = (0,0,0)
        sgF.write()
    if number>=48 and number<56:
        number=number-48
        sgG[number] = (0,0,0)
        sgG.write()
    

def segment_on(number,color,luminosity):
    ledMin = ((number-1)*8)+1
    ledMax = (number*8)+1
    for led in range(ledMin, ledMax):
        led_on(led,color,luminosity)

def segment_off(number):
    ledMin = ((number-1)*8)+1
    ledMax = (number*8)+1
    for led in range(ledMin,ledMax):
        led_off(led)
 
def afficheur_off():
    for segment in range(1,segmentsAfficheur+1):
        segment_off(segment)
 
def afficheur_set(symbol,color,luminosity):
    if symbol=="0":
        septSeg=[1,1,1,1,1,1,0]
    elif symbol=="1":
        septSeg=[0,1,1,0,0,0,0]
    elif symbol=="2":
        septSeg=[1,1,0,1,1,0,1]
    elif symbol=="3":
        septSeg=[1,1,1,1,0,0,1]
    elif symbol=="4":
        septSeg=[0,1,1,0,0,1,1]
    elif symbol=="5":
        septSeg=[1,0,1,1,0,1,1]
    elif symbol=="6":
        septSeg=[1,0,1,1,1,1,1]
    elif symbol=="7":
        septSeg=[1,1,1,0,0,0,0]
    elif symbol=="8":
        septSeg=[1,1,1,1,1,1,1]
    elif symbol=="9":
        septSeg=[1,1,1,1,0,1,1]
    elif symbol=="o":
        septSeg=[0,0,1,1,1,0,1]
    elif symbol=="c":
        septSeg=[0,0,0,1,1,0,1]
    elif symbol=="u":
        septSeg=[0,0,1,1,1,0,0]
    elif symbol=="-":
        septSeg=[0,0,0,0,0,0,1]
    elif symbol=="n":
        septSeg=[0,0,1,0,1,0,1]
    elif symbol=="U":
        septSeg=[0,1,1,1,1,1,0]
    else:
        septSeg=[0,0,0,0,0,0,0]
    for pointeur in range(0,segmentsAfficheur):
        if septSeg[pointeur]==1:
            segment_on(pointeur+1,color,luminosity)
        elif septSeg[pointeur]==0:
            segment_off(pointeur+1)
        else:
            segment_off(pointeur+1)

def raw_on(y,color,luminosity):
    if y==1:
        segment_on(y,color,luminosity)
    if y>1 and y<10:
        led_on(y+7,color,luminosity)
        led_on(50-y,color,luminosity)
    if y==10:
        segment_on(7,color,luminosity)
    if y>10 and y<19:
        led_on(y+6,color,luminosity)
        led_on(51-y,color,luminosity)
    if y==19:
        segment_on(4,color,luminosity)      

def raw_off(y):
    if y==1:
        segment_off(y)
    elif y>1 and y<10:
        led_off(y+7)
        led_off(50-y)
    elif y==10:
        segment_off(7)
    elif y>10 and y<19:
        led_off(y+6)
        led_off(51-y)
    elif y==19:
        segment_off(4) 

def column_on(x,color,luminosity):
    if x==1:
        segment_on(5,color,luminosity)
        segment_on(6,color,luminosity)
    elif x>1 and x<10:
        led_on(x-1,color,luminosity)
        led_on(47+x,color,luminosity)
        led_on(34-x,color,luminosity)
    elif x==10:
        segment_on(2,color,luminosity)
        segment_on(3,color,luminosity)
        
def column_off(x):
    if x==1:
        segment_off(5)
        segment_off(6)
    elif x>1 and x<10:
        led_off(x-1)
        led_off(x+47)
        led_off(34-x)
    elif x==10:
        segment_off(2)
        segment_off(3)        

def diag45_on(number, color,luminosity):
    if number>=1 and number<=8:
        led_on(number,color,luminosity)
        led_on(49-number,color,luminosity)
    if number>8 and number<17:
        led_on(number,color,luminosity)
        led_on(40+number,color,luminosity)
        led_on(49-number,color,luminosity)
    if number>=17 and number<=24:
        led_on(number,color,luminosity)
        led_on(49-number,color,luminosity)        

def diag45_off(number):
    if number>=1 and number<=8:
        led_off(number)
        led_off(49-number)
    if number>8 and number<17:
        led_off(number)
        led_off(40+number)
        led_off(49-number)
    if number>=17 and number<=24:
        led_off(number)
        led_off(49-number)
        
def diag270_on(number, color,luminosity):
    if number>=1 and number<=8:
        led_on(9-number,color,luminosity)
        led_on(number+8,color,luminosity)
    if number>8 and number<17:
        led_on(65-number,color,luminosity)
        led_on(57-number,color,luminosity)
        led_on(number+8,color,luminosity)
    if number>=17 and number<=24:
        led_on(57-number,color,luminosity)
        led_on(number+8,color,luminosity)        

def diag270_off(number):
    if number>=1 and number<=8:
        led_off(9-number)
        led_off(number+8)
    if number>8 and number<17:
        led_off(65-number)
        led_off(57-number)
        led_off(number+8)
    if number>=17 and number<=24:
        led_off(57-number)
        led_off(number+8)