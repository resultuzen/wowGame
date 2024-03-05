import RPi.GPIO as GPIO
import time

# Pin numarasını belirtin
buton_pin = 17

# GPIO modunu belirleme
GPIO.setmode(GPIO.BCM)

# Pin'i giriş olarak ayarlama ve pull-down direnci etkinleştirme
GPIO.setup(buton_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

while True:
    if GPIO.input(buton_pin) == GPIO.HIGH:
        print("Hey")
