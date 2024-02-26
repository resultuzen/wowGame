import RPi.GPIO as GPIO
import time

# Pin numarasını belirtin
buton_pin = 17

# GPIO modunu belirleme
GPIO.setmode(GPIO.BCM)

# Pin'i giriş olarak ayarlama ve pull-down direnci etkinleştirme
GPIO.setup(buton_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Interrupt tetikleyiciyi ayarlama fonksiyonu
def button_callback(channel):
    print("Button pressed on pin {}".format(channel))

# GPIO üzerinde interrupt tetikleyiciyi tanımlama
GPIO.add_event_detect(buton_pin, GPIO.RISING, callback=button_callback, bouncetime=300)

try:
    print("Press Ctrl+C to exit")
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    pass

finally:
    # GPIO temizleme
    GPIO.cleanup()
