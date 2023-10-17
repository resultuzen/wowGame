import RPi.GPIO as GPIO
import time

# GPIO pinlerini ayarla
ENKODER1_DT = 31
ENKODER1_CLK = 29
ENKODER2_DT = 35
ENKODER2_CLK = 33

# GPIO pinlerini giriş olarak ayarla
GPIO.setmode(GPIO.BCM)
GPIO.setup(ENKODER1_DT, GPIO.IN)
GPIO.setup(ENKODER1_CLK, GPIO.IN)
GPIO.setup(ENKODER2_DT, GPIO.IN)
GPIO.setup(ENKODER2_CLK, GPIO.IN)

# Enkoder değerlerini izlemek için değişkenler
enkoder1_count = 0
enkoder2_count = 0

# Enkoder 1 için dönüş izlemesi
def enkoder1_turn(channel):
    global enkoder1_count
    enkoder1_count += 1

# Enkoder 2 için dönüş izlemesi
def enkoder2_turn(channel):
    global enkoder2_count
    enkoder2_count += 1

# Kesme işlevlerini tanımla
GPIO.add_event_detect(ENKODER1_CLK, GPIO.FALLING, callback=enkoder1_turn)
GPIO.add_event_detect(ENKODER2_CLK, GPIO.FALLING, callback=enkoder2_turn)

# Ana döngü
try:
    while True:
        # Her iki enkoderin dönüş sayısını görüntüle
        print(f"Enkoder 1 Dönüş Sayısı: {enkoder1_count}")
        print(f"Enkoder 2 Dönüş Sayısı: {enkoder2_count}")
        time.sleep(1)

except KeyboardInterrupt:
    # Kesme alındığında temizlik yap
    GPIO.cleanup()
