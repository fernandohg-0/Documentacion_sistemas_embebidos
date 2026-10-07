from gpiozero import LED
from time import sleep

rojo = LED(17)
amarillo = LED(27)
verde = LED(22)

print("Semáforo iniciado. Presiona Ctrl+C para detener.")

try:
    while True:

        # ROJO
        rojo.on()
        amarillo.off()
        verde.off()
        print("ROJO")
        sleep(3)

        # AMARILLO
        rojo.off()
        amarillo.on()
        verde.off()
        print("AMARILLO")
        sleep(3)

        # VERDE
        rojo.off()
        amarillo.off()
        verde.on()
        print("VERDE")
        sleep(3)

except KeyboardInterrupt:
    rojo.off()
    amarillo.off()
    verde.off()
    print("\nSemáforo detenido.")
