from .. import GPIO_Library as gpio
from .. import PWM_Library as pwm

# regist gpio pin and pwm channel
def set_device(in1, in2, channel):
    pwm.export(channel)
    pwm.set_enable(0)

    gpio.export(in1)
    gpio.set_direction(in1, 'out')
    gpio.export(in2)
    gpio.set_direction(in2, 'out')

# select motor rotation and turn on
def motor_control(in1, in2, rotation, channel):
    if rotation == "forward":
        gpio.set_value(in1 , 1)
        gpio.set_value(in2 , 0)
    elif rotation == "backward":
        gpio.set_value(in1 , 0)
        gpio.set_value(in2 , 1)
    else :
        gpio.set_value(in1 , 0)
        gpio.set_value(in2 , 0)
    pwm.set_enable(channel, 1)

# setting motor speed
def set_speed(channel, period, cycle):
    pwm.set_period_ns(period)
    pwm.set_cycle_ns(channel, cycle)

# unregist gpio pin and pwm channel
def quit_device(in1, in2, channel):
    gpio.unexport(in1)
    gpio.unexport(in2)
    pwm.unexport(channel)