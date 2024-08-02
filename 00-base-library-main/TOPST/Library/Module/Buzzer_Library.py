from .. import GPIO_Library
from .. import PWM_Library

#GPIO Buzzer
# Set a buzzer gpio
def set_buzzer_gpio(gpio_pin):
    GPIO_Library.export(gpio_pin)
    GPIO_Library.set_direction(gpio_pin, "out")

# Quit a buzzer gpio
def quit_buzzer_gpio(gpio_pin):
    GPIO_Library.unexport(gpio_pin)

# make a buzzer sound
def turn_on_gpio(gpio_pin):
    GPIO_Library.set_value(gpio_pin , 1)

# make a buzzer quiet
def turn_off_gpio(gpio_pin):
    GPIO_Library.set_value(gpio_pin , 0)

#PWM Buzzer
# Set a buzzer pwm
def set_buzzer_pwm(channel):
    PWM_Library.export(channel)

# Quit a buzzer pwm
def quit_buzzer_pwm(channel):
    PWM_Library.unexport(channel)

# Set pwm pulse's hz
def set_tone_pwm(channel, hz):
    PWM_Library.set_period_sec(channel, hz)
    PWM_Library.set_cycle_sec(channel, hz)    

# make a buzzer sound
def turn_on_pwm(channel):
    PWM_Library.set_enable(channel, 1)

# make a buzzer quiet
def turn_off_pwm(channel):
    PWM_Library.set_enable(channel, 0)