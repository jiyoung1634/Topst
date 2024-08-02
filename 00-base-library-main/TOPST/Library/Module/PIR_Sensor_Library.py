from .. import GPIO_Library as gpio

# regist device gpio pin
def set_device(gpio_pin):
    gpio.export(gpio_pin)
    gpio.set_direction(gpio_pin, 'in')

# get data from gpio_pin
def read_data(gpio_pin):
    return gpio.get_value(gpio_pin)

# unregist device gpio pin
def quit_device(gpio_pin):
    gpio.unexport(gpio_pin)