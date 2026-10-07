from gpiozero import LED
from time import sleep

led = LED(17)

print("LED iniciado. Presiona Ctrl+C para detener.")

try:
    while True:
        led.on()
        print("LED ON")
        sleep(5)

        led.off()
        print("LED OFF")
        sleep(5)

except KeyboardInterrupt:
    led.off()
    print("\nPrograma detenido.")
