from .. import GPIO_Library as gpio

# set gpio pin for use device
def set_device(gpio_pin):
    gpio.export(gpio_pin)
    gpio.set_direction(gpio_pin, "in")

# get value from device
def get_value(gpio_pin):
    value = gpio.get_value(gpio_pin)
    if value == 1:
        return True
    else:
        return False

def quit_device(gpio_pin):
    gpio.unexport(gpio_pin)