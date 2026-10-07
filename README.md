# Documentación de sistemas embebidos

Prácticas en una **Raspberry Pi 5**, controlada desde la laptop por Ethernet y SSH. Los programas viven en `~/teseom`, dentro del entorno virtual `.venv`, y se ejecutan con el usuario `aqua`.

Los videos se publicaron **sin audio**. El código usado está en la carpeta [`codigo`](codigo).

## Equipo

- Laptop con Windows
- Raspberry Pi 5
- Cable Ethernet directo entre las dos
- Protoboard, cables Dupont y resistencias de 220 Ω a 330 Ω
- 1 LED para la prueba de encendido y apagado
- 3 LED (rojo, amarillo y verde) para el semáforo
- LCD 20x4 con adaptador I²C de 4 pines: `GND`, `VCC`, `SDA`, `SCL`

## Cómo se conectó la laptop con la Raspberry Pi

La Pi no se programó con teclado ni monitor. La laptop entra por SSH a través de un cable Ethernet con IP fija. No hace falta Wi-Fi ni Internet para esa conexión.

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

La IP de la Pi quedó guardada en NetworkManager con el perfil `netplan-eth0`. Por eso se puede desconectar el cable, transportar los dos equipos y volver a trabajar sin reconfigurar la Pi:

1. Conectar de nuevo el Ethernet.
2. Encender la laptop y la Pi.
3. En CMD de Windows:

```text
ssh aqua@192.168.50.2
```

La sesión abre directo en:

```text
aqua@aqua:~ $
```

La laptop tiene que conservar la IP `192.168.50.1` en ese adaptador. Si Windows lo regresa a DHCP, el SSH deja de entrar hasta volver a poner esa IP.

Desde esa sesión se está dentro de Linux de la Pi. `nano` y `python` corren en la Pi, y los GPIO que se usan son los de la Pi.

```text
cd ~/teseom
source .venv/bin/activate
nano led.py
python led.py
```

En `nano`, guardar es `Ctrl+O`, Enter y `Ctrl+X`.

## Entorno de Python

Comprobación inicial:

```text
python3 --version
sudo apt update
sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv
```

El entorno se creó así:

```text
mkdir ~/teseom
cd ~/teseom
python3 -m venv .venv
source .venv/bin/activate
```

Librerías instaladas dentro del entorno:

```text
pip install gpiozero
pip install smbus2
```

`gpiozero` controla los LED. `smbus2` habla por I²C con el LCD. La librería `RPLCD` no se pudo instalar: la Ethernet entre laptop y Pi no tiene Internet, y `pip` falló con `Temporary failure in name resolution`. El LCD se manejó con un controlador propio escrito sobre `smbus2`, que ya estaba instalado.

Antes de la pantalla se comprobó:

```text
python -c "import smbus2; print('smbus2 OK')"
ls /dev/i2c-*
```

Resultado: `smbus2 OK` y los buses `/dev/i2c-1`, `/dev/i2c-13` y `/dev/i2c-14`. El LCD responde en el bus 1.

## 1. Encender y apagar un LED

El LED usa **GPIO17**, pin físico **11**. La tierra es el pin físico **6**. Entre el GPIO y el LED va una resistencia de 220 Ω a 330 Ω. El LED no se conecta directo al GPIO.

| Señal | Pin físico | Hacia dónde |
| --- | --- | --- |
| GPIO17 | 11 | Resistencia y después la pata larga (+) del LED |
| GND | 6 | Pata corta (−) del LED |

```text
Pin 11 (GPIO17) ── resistencia 220–330 Ω ──►|── GND (pin 6)
                                            LED
```

Programa: [`codigo/led.py`](codigo/led.py)

En la Pi:

```text
cd ~/teseom
source .venv/bin/activate
python led.py
```

El LED queda **5 segundos encendido** y **5 segundos apagado**. La terminal imprime `LED ON` y `LED OFF`. Con `Ctrl+C` se apaga el LED y aparece `Programa detenido.`

Video, sin audio: [evidencia/led/video_encendido_apagado.mp4](evidencia/led/video_encendido_apagado.mp4)

## 2. Semáforo

Tres LED. Cada uno tiene su resistencia de 220 Ω a 330 Ω. Los tres comparten la tierra del pin físico 6. La pata larga va hacia la resistencia y de ahí al GPIO. La pata corta va a GND.

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

Programa: [`codigo/semaforo.py`](codigo/semaforo.py)

```text
python semaforo.py
```

Solo uno está encendido a la vez, **3 segundos** cada color, en este orden: rojo, amarillo, verde. La terminal imprime `ROJO`, `AMARILLO` y `VERDE`. Con `Ctrl+C` se apagan los tres y aparece `Semáforo detenido.`

Video, sin audio: [evidencia/semaforo/video_secuencia.mp4](evidencia/semaforo/video_secuencia.mp4)

## 3. Hola mundo en el LCD

El módulo es un LCD 20x4 con adaptador I²C. Los cuatro pines, confirmados en el módulo, son `GND`, `VCC`, `SDA` y `SCL`. Se conectó con la Raspberry apagada.

| LCD | Raspberry Pi 5 | Pin físico |
| --- | --- | --- |
| GND | GND | 6 |
| VCC | 5 V | 2 |
| SDA | GPIO2 / SDA | 3 |
| SCL | GPIO3 / SCL | 5 |

`VCC` va a 5 V, no a un GPIO. `SDA` y `SCL` van a los pines I²C, no a 5 V. GND y VCC no se intercambian.

I²C se habilitó con `sudo raspi-config` en **Interface Options → I2C → Enable**, y después `sudo reboot`. Para volver a entrar:

```text
ssh aqua@192.168.50.2
cd ~/teseom
source .venv/bin/activate
```

Detección:

```text
sudo apt install -y i2c-tools
sudo i2cdetect -y 1
```

En la fila `20` apareció `27`. La dirección del LCD es **0x27**, en el bus **1**.

Como `RPLCD` no se pudo bajar, el programa [`codigo/lcd.py`](codigo/lcd.py) inicializa el controlador HD44780 en modo de 4 bits a través del adaptador PCF8574 y escribe en la primera línea.

```text
python lcd.py
```

Salida en terminal:

```text
LCD funcionando.
Se muestra: hola TESOEM
```

En la pantalla se lee `hola TESOEM`. El programa se queda en espera para que el texto no se borre al salir. `Ctrl+C` lo detiene.

![LCD mostrando hola TESOEM](evidencia/lcd/foto_pantalla_hola_tesoem.jpg)

![Terminal con python lcd.py](evidencia/lcd/foto_terminal_lcd.jpg)

![Montaje: laptop, Raspberry Pi y LCD](evidencia/lcd/foto_montaje_general.jpg)

## Terminal del LED y del semáforo

Estas dos capturas juntan las dos primeras prácticas en la misma toma, por eso no se cortaron.

El video dura unos 9 segundos. En la laptop se ve la salida `LED ON` / `LED OFF` y `Programa detenido.`, y después `python semaforo.py` con `ROJO`, `AMARILLO` y `VERDE`. Al fondo está la protoboard. No tiene audio.

Video: [evidencia/terminal/video_led_y_semaforo.mp4](evidencia/terminal/video_led_y_semaforo.mp4)

![Terminal del LED y del semáforo](evidencia/terminal/foto_terminal_led_y_semaforo.jpg)

## Archivos

| Qué | Dónde |
| --- | --- |
| LED, 5 s encendido y 5 s apagado | [`codigo/led.py`](codigo/led.py) |
| Semáforo, 3 s por color | [`codigo/semaforo.py`](codigo/semaforo.py) |
| LCD, texto `hola TESOEM` en `0x27` | [`codigo/lcd.py`](codigo/lcd.py) |
| Video del LED | [evidencia/led/video_encendido_apagado.mp4](evidencia/led/video_encendido_apagado.mp4) |
| Video del semáforo | [evidencia/semaforo/video_secuencia.mp4](evidencia/semaforo/video_secuencia.mp4) |
| Foto del texto en el LCD | [evidencia/lcd/foto_pantalla_hola_tesoem.jpg](evidencia/lcd/foto_pantalla_hola_tesoem.jpg) |
| Foto de la terminal del LCD | [evidencia/lcd/foto_terminal_lcd.jpg](evidencia/lcd/foto_terminal_lcd.jpg) |
| Foto del montaje completo | [evidencia/lcd/foto_montaje_general.jpg](evidencia/lcd/foto_montaje_general.jpg) |
| Video de las dos terminales | [evidencia/terminal/video_led_y_semaforo.mp4](evidencia/terminal/video_led_y_semaforo.mp4) |
| Foto de las dos terminales | [evidencia/terminal/foto_terminal_led_y_semaforo.jpg](evidencia/terminal/foto_terminal_led_y_semaforo.jpg) |
