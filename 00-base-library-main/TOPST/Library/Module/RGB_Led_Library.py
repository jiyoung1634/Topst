from .. import GPIO_Library as gpio

# regist RGB_LED
def set_device(rgb_pins):
    for pin in rgb_pins:
        gpio.export(pin)
        gpio.set_direction(pin, 'out')
        gpio.set_value(pin, 0)

# unregist RGB_LED
def quit_device(rgb_pins):
    for pin in rgb_pins:
        gpio.unexport(pin)

# set red, green, blue value
def set_value(rgb_pins, values):
    for i in len(rgb_pins):
        gpio.set_value(rgb_pins[i], values[i])