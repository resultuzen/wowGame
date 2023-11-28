import RPi.GPIO as GPIO
import time

button_pin = 21

# GPIO ayarları
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    print("Buton okuma başlatıldı. Çıkış yapmak için Ctrl+C'ye basın.")

    while True:
        button_state = GPIO.input(button_pin)

        if button_state == GPIO.LOW:
            print("Buton basıldı!")

        time.sleep(0.1)

finally:
    # GPIO pinlerini temizle
    GPIO.cleanup()
