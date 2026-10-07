from smbus2 import SMBus
from time import sleep

LCD_ADDR = 0x27
I2C_BUS = 1

# Bits del adaptador I2C
LCD_BACKLIGHT = 0x08
ENABLE = 0x04

# Comandos LCD
LCD_CLEAR = 0x01
LCD_HOME = 0x02
LCD_FUNCTIONSET = 0x28
LCD_DISPLAY_ON = 0x0C
LCD_ENTRYMODE = 0x06


def lcd_write_byte(bus, data):
    bus.write_byte(LCD_ADDR, data | LCD_BACKLIGHT)


def lcd_pulse_enable(bus, data):
    lcd_write_byte(bus, data | ENABLE)
    sleep(0.0005)
    lcd_write_byte(bus, data & ~ENABLE)
    sleep(0.0005)


def lcd_send_nibble(bus, nibble, mode=0):
    data = nibble | mode
    lcd_write_byte(bus, data)
    lcd_pulse_enable(bus, data)


def lcd_send_byte(bus, value, mode=0):
    lcd_send_nibble(bus, value & 0xF0, mode)
    lcd_send_nibble(bus, (value << 4) & 0xF0, mode)


def lcd_command(bus, command):
    lcd_send_byte(bus, command)
    sleep(0.002)


def lcd_data(bus, value):
    lcd_send_byte(bus, value, 0x01)


def lcd_init(bus):
    sleep(0.05)

    lcd_send_nibble(bus, 0x30)
    sleep(0.005)

    lcd_send_nibble(bus, 0x30)
    sleep(0.001)

    lcd_send_nibble(bus, 0x30)
    sleep(0.001)

    lcd_send_nibble(bus, 0x20)

    lcd_command(bus, LCD_FUNCTIONSET)
    lcd_command(bus, LCD_DISPLAY_ON)
    lcd_command(bus, LCD_CLEAR)
    lcd_command(bus, LCD_ENTRYMODE)


def lcd_print(bus, text):
    for char in text:
        lcd_data(bus, ord(char))


try:
    with SMBus(I2C_BUS) as bus:

        lcd_init(bus)

        # Primera línea
        lcd_print(bus, "hola TESOEM")

        print("LCD funcionando.")
        print("Se muestra: hola TESOEM")

        while True:
            sleep(1)

except KeyboardInterrupt:
    print("\nPrograma detenido.")
