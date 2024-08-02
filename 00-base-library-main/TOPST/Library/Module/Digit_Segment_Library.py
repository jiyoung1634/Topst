import GPIO_Library as gpio

# regist segment_pins and digit_pins
def set_device(segment_pins, digit_pins):
    for pin in segment_pins:
        gpio.export(pin)
        gpio.set_direction(pin, 'out')
        gpio.set_value(pin, 0)
    for pin in digit_pins:
        gpio.export(pin)
        gpio.set_direction(pin, 'out')
        gpio.set_value(pin, 0)

# unregist segment pins and digit pins
def quit_device(segment_pins, digit_pins):
    for pin in segment_pins:
        gpio.unexport(pin)
    for pin in digit_pins:
        gpio.unexport(pin)

# turn on digit and segment
def turn_on_digit(segment_pins, digit_pins):
    for pin in digit_pins:
        gpio.set_value(pin, 0)
    for pin in segment_pins:
        gpio.set_value(pin, 1)

# turn off digit and segment
def turn_off_digit(segment_pins, digit_pins):
    for pin in digit_pins:
        gpio.set_value(pin, 1)
    for pin in segment_pins:
        gpio.set_value(pin, 0)

# turn off all display and turn on data
def display(segment_pins, digit_pins, data_segment, data_digit):
    turn_off_digit(digit_pins, segment_pins)
    turn_on_digit(data_segment, data_digit)