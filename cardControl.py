import RPi.GPIO as GPIO

kartOkuyucuPin = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(kartOkuyucuPin, GPIO.IN)

while True:
    
    print(GPIO.input(kartOkuyucuPin))
