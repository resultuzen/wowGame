import RPi.GPIO as GPIO

# Kullanmak istediğiniz GPIO pin numarasını buraya girin
buton_pin = 21

# GPIO ayarları
GPIO.setmode(GPIO.BCM)
GPIO.setup(buton_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    print("Buton okuma başladı. Çıkış yapmak için Ctrl+C'ye basın.")
    while True:
        # Buton durumunu oku
        buton_durumu = GPIO.input(buton_pin)

        # Buton basıldığında durumu 0, basılmadığında durumu 1 olacaktır
        if buton_durumu == 0:
            print("Buton basıldı!")
        else:
            print("Buton bırakıldı!")

except KeyboardInterrupt:
    print("Program kapatılıyor.")

finally:
    # GPIO pinlerini temizle
    GPIO.cleanup()
