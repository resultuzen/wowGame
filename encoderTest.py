import time
from encoder import Encoder
import RPi.GPIO as GPIO
import os
import sys
import random
import board
import time

# GPIO pinlerini ayarla
solEnkoderDataPin = 19
solEnkoderClockPin = 13
sagEnkoderDataPin = 6
sagEnkoderClockPin = 5

GPIO.setmode(GPIO.BCM)

solEncoder = Encoder(solEnkoderDataPin, solEnkoderClockPin)
sagEncoder = Encoder(sagEnkoderDataPin, sagEnkoderClockPin)

# Enkoderlerin değerlerini tutmak için değişkenler
solEnkoderDegeri = 0
sagEnkoderDegeri = 0

while True:    
    
    if not(sagOyuncu.top <= 0) or not(sagOyuncu.bottom >= height):
        sagEnkoderDegeri = sagEncoder.getValue()

    if sagOyuncu.top <= 0:
        sagEnkoderDegeri = -25 #Sağ enkoderin minumum değeri öğrenilecek, hatta hesaplama yaptırılırsa daha iyi olur!

    if sagOyuncu.bottom >= height:
        sagEnkoderDegeri = 25 #Sağ enkoderin maksimum değeri öğrenilecek, hatta hesaplama yaptırılırsa daha iyi olur!

    if not(solOyuncu.top <= 0) or not(solOyuncu.bottom >= height):
        solEnkoderDegeri = solEncoder.getValue()

    if solOyuncu.top <= 0:
        solEnkoderDegeri = -25 #Sol enkoderin minumum değeri öğrenilecek, hatta hesaplama yaptırılırsa daha iyi olur!

    if solOyuncu.bottom >= height:
        solEnkoderDegeri = 25 #Sol enkoderin maksimum değeri öğrenilecek, hatta hesaplama yaptırılırsa daha iyi olur!

    #sagEnkoderDegeri = sagEncoder.getValue()
    #solEnkoderDegeri = solEncoder.getValue()

    print("Sağ:",sagEnkoderDegeri)
    print("Sol:",solEnkoderDegeri)
