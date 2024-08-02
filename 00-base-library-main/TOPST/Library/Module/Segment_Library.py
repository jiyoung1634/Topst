from .. import GPIO_Library as gpio

num_array=[
    [0,1,2,3,4,5], #0
    [1,2], #1
    [0,1,3,4,6], #2
    [0,1,2,3,6], #3
    [1,2,5,6], #4
    [0,2,3,5,6], #5
    [0,2,3,4,5,6], #6
    [0,1,2], #7
    [0,1,2,3,4,5,6], #8
    [0,1,2,3,5,6] #9
]

# regist device gpio pins
def set_device(gpio_pins):
    for pin in gpio_pins:
        gpio.export(pin)
        gpio.set_direction(pin, 'out')
        gpio.set_value(pin, 0)

# unregist device gpio pins
def quit_device(gpio_pins):
    for pin in gpio_pins:
        gpio.unexport(pin)

# turn off all display
def display_off(gpio_pins):
    for pin in gpio_pins:
        gpio.set_value(pin, 0)

# display number
def display_num(gpio_pins, num):
    for i in num_array[num]:
        gpio.set_value(gpio_pins[i], 1)

# display data
def display_on(data):
    for pin in data:
        gpio.set_value(pin, 1)