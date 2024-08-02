from .. import GPIO_Library
from .. import PWM_Library

# GPIO LED
# led setting
def set_led_gpio(gpio_pin):
    GPIO_Library.export(gpio_pin)
    GPIO_Library.set_direction(gpio_pin, "out")

# led exiting
def quit_led_gpio(gpio_pin):
    GPIO_Library.unexport(gpio_pin)

# turn on led
def turn_on_gpio(gpio_pin):
    GPIO_Library.set_value(gpio_pin, 1)
    
# turn off led
def turn_off_gpio(gpio_pin):
    GPIO_Library.set_value(gpio_pin, 0)

#PWM LED
#led Setting
def set_led_pwm(channel):
    PWM_Library.export(channel)

# led exiting
def quit_led_pwm(channel):
    PWM_Library.unexport(channel)

# set led's pulse by second unit
def set_led_cycle(channel, second, cycle):
    PWM_Library.set_period_sec(channel, second)
    PWM_Library.set_cycle_sec(channel, cycle)
    
# set led's pulse by nano second unit
def set_led_cycle_ns(channel, nano_second, nano_cycle):
    PWM_Library.set_period_ns(channel, nano_second)
    PWM_Library.set_cycle_ns(channel, nano_cycle)

# turn on led
def turn_on_pwm(channel):
    PWM_Library.set_enable(channel, 1)

# turn off led
def turn_off_pwm(channel):
    PWM_Library.set_enable(channel, 0)