from .. import GPIO_Library as gpio
import time


pins= [] # list of input pins

# setting input pin for use device
def set_driver(input_pins):
    for pin in input_pins:
        gpio.export(pin)
        gpio.set_direction(pin, "out")
        gpio.set_value(pin, 0)
        pins.append(pin)

# select location by gpio pin's output value
def set_location(input_pin, input_pin2 = -1):
    for pin in pins:
        if(pin == input_pin):
            gpio.set_value(pin, 1)
        elif(input_pin2 != -1 and pin == input_pin2):
            gpio.set_value(pin, 1)
        else:
            gpio.set_value(pin, 0)

# rotate motor
def rotation(step_count, direction):
    step_counter = 0
    for i in range(0,step_count):
        if step_counter%2 ==0:
                set_location(pins[step_counter//2])
        else:
            set_location(pins[step_counter//2],pins[(step_counter//2+1)%4])
        if direction == True:
            step_counter = (step_counter -1)%8
        else:
            step_counter = (step_counter +1)%8
        time.sleep(0.01)

def quit_driver(input_pins):
    for pin in input_pins:
        gpio.unexport(pin)
        pins.remove(pin)