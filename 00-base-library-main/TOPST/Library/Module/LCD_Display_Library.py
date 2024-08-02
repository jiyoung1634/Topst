from .. import GPIO_Library as gpio
import time

# bytes for init lcd
init_bytes=[
    0x33, 0x32, 0x28, 0x0C, 0x06, 0x01
]
# bytes for select line of lcd
line_bytes = [0x80, 0xC0]

#gpio_pins = [LCD_RS, LCD_E, D4, D5, D6, D7]
def set_device(gpio_pins):
    for pin in gpio_pins:
        gpio.export(pin)
        gpio.set_direction(pin, 'out')
    for byte in init_bytes:
        byte_transfer(gpio_pins, byte, 0)

def quit_device(gpio_pins):
    for pin in gpio_pins:
        gpio.unexport(pin)

# transfer byte to lcd display
def byte_transfer(gpio_pins, byte, mode):
    gpio.set_value(gpio_pins[0], mode)
    for pin in range (2,6):
        gpio.set_value(pin, 0)
    
    # transfer high 4 bit
    if byte & 0x10 == 0x10:
        gpio.set_value(gpio_pins[2], 1)
    if byte & 0x20 == 0x20:
        gpio.set_value(gpio_pins[3], 1)
    if byte & 0x40 == 0x40:
        gpio.set_value(gpio_pins[4], 1)
    if byte & 0x80 == 0x80:
        gpio.set_value(gpio_pins[5], 1)
    toggle(gpio_pins[1])

    for pin in range (2,6):
        gpio.set_value(pin, 0)
    # transfer low 4 bit
    if byte & 0x01 == 0x01:
        gpio.set_value(gpio_pins[2], 1)
    if byte & 0x02 == 0x02:
        gpio.set_value(gpio_pins[3], 1)
    if byte & 0x04 == 0x04:
        gpio.set_value(gpio_pins[4], 1)
    if byte & 0x08 == 0x08:
        gpio.set_value(gpio_pins[5], 1)
    toggle(gpio_pins[1])

# toggle for lcd display
def toggle(gpio_e):
    time.sleep(0.0005)
    gpio.set_value(gpio_e, "1")
    time.sleep(0.0005)
    time.sleep(gpio_e, "0")
    time.sleep(0.0005)

# display data on lcd display
def display_on(data, line):
    message = str(data).ljust(16, " ")
    byte_transfer(line_bytes[line], 0)

    for i in range(16):
        byte_transfer(ord(message[i]), 1)