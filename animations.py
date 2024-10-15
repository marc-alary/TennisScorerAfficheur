from afficheur import *
from time import sleep

def wavesymbol(symbol,color):
    change=10
    while change <=70:
        afficheur_set(symbol, color, change)
        change=change+5
    change=75
    while change >=10:
        afficheur_set(symbol, color, change)
        change=change-5  

def falldown(color,luminosity):
    tempo=0.3
    for raw in range (1,20):
        raw_on(raw,color,luminosity)
        sleep(tempo)
        raw_off(raw)
        if raw==2:
            tempo=tempo-0.1
        if raw==4:
            tempo=tempo-0.1
        if raw==6:
            tempo=tempo-0.05
        if raw==8:
            tempo=tempo-0.01
        if raw==10:
            tempo=tempo-0.01
            
def riseup(color,luminosity):
    tempo=0.3
    for raw in range (19,0,-1):
        raw_on(raw,color,luminosity)
        sleep(tempo)
        raw_off(raw)
        if raw==18:
            tempo=tempo-0.1
        if raw==16:
            tempo=tempo-0.1
        if raw==14:
            tempo=tempo-0.05
        if raw==11:
            tempo=tempo-0.01
        if raw==10:
            tempo=tempo-0.01