from .. import GPIO_Library

# setting gpio_pin for use device
def set_ball_tilt_sensor(gpio_pin):
    GPIO_Library.export(gpio_pin)
    GPIO_Library.set_direction(gpio_pin, "in")
    GPIO_Library.set_edge(gpio_pin, "both")

# get sensor value high or low
def get_sensor_value(gpio_pin):
    return GPIO_Library.get_value(gpio_pin)

# unexport device
def quit_ball_tile_sensor(gpio_pin):
    GPIO_Library.unexport(gpio_pin)