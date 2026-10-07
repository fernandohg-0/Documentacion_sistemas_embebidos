# P2_SemaforoLeds

Semáforo con tres LED en una Raspberry Pi 5. Cada color permanece encendido 3 segundos y después pasa al siguiente: rojo, amarillo y verde.

El programa está en [`semaforo.py`](semaforo.py). La misma documentación está en [`P2_SemaforoLeds.docx`](P2_SemaforoLeds.docx).

## Equipo

- Laptop con Windows
- Raspberry Pi 5
- Cable Ethernet directo entre las dos
- Protoboard y cables Dupont
- 3 LED: rojo, amarillo y verde
- 3 resistencias de 220 Ω a 330 Ω

## Conexión de la laptop con la Raspberry Pi

La Pi se programa desde la laptop por SSH. No hace falta Wi-Fi ni Internet.

| Equipo | IP |
| --- | --- |
| Laptop | `192.168.50.1` |
| Raspberry Pi | `192.168.50.2` |

```text
Laptop  192.168.50.1
   │
   │  Ethernet
   │
Raspberry Pi  192.168.50.2
```

La IP de la Pi quedó guardada en NetworkManager con el perfil `netplan-eth0`. Para entrar, en CMD:

```text
ssh aqua@192.168.50.2
```

La laptop tiene que conservar la IP `192.168.50.1`. Si Windows cambia ese adaptador a DHCP, hay que volver a fijar la IP.

## Entorno

```text
cd ~/teseom
source .venv/bin/activate
```

Los LED se controlan con `gpiozero`, instalado en ese entorno.

## Conexión de los tres LED

Cada LED tiene su propia resistencia de 220 Ω a 330 Ω. Los tres comparten la tierra del pin físico 6. La pata larga (+) va a la resistencia y de ahí al GPIO. La pata corta (−) va a GND. Ningún LED se conecta directo al GPIO.

| LED | GPIO | Pin físico |
| --- | --- | --- |
| Rojo | GPIO17 | 11 |
| Amarillo | GPIO27 | 13 |
| Verde | GPIO22 | 15 |
| Tierra común | GND | 6 |

```text
GPIO17 (pin 11) ──[220 Ω]──►|── GND     rojo
GPIO27 (pin 13) ──[220 Ω]──►|── GND     amarillo
GPIO22 (pin 15) ──[220 Ω]──►|── GND     verde
GND = pin físico 6
```

## Programa

Archivo: `semaforo.py`.

```python
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
```

## Ejecución

```text
cd ~/teseom
source .venv/bin/activate
python semaforo.py
```

La terminal imprime:

```text
Semáforo iniciado. Presiona Ctrl+C para detener.
ROJO
AMARILLO
VERDE
ROJO
AMARILLO
VERDE
```

Solo un LED está encendido a la vez, 3 segundos por color. `Ctrl+C` apaga los tres y muestra `Semáforo detenido.`

## Evidencia

El video no tiene audio. Dura unos 5 segundos y es un acercamiento de la protoboard: al inicio está el rojo y después pasa al verde.

Video: [evidencia/video_secuencia.mp4](evidencia/video_secuencia.mp4)

La toma de la laptop también muestra esta ejecución, después de la del LED: `python semaforo.py` y el ciclo `ROJO`, `AMARILLO`, `VERDE`.

Video: [evidencia/video_led_y_semaforo.mp4](evidencia/video_led_y_semaforo.mp4)

![Terminal del LED y del semáforo](evidencia/foto_terminal_led_y_semaforo.jpg)
