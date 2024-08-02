import sys
import os
import time

GPIO_EXPORT_PATH = "/sys/class/gpio/export"
GPIO_UNEXPORT_PATH = '/sys/class/gpio/unexport'
GPIO_DIRECTION_PATH_TEMPLATE = '/sys/class/gpio/gpio{}/direction'
GPIO_VALUE_PATH_TEMPLATE = '/sys/class/gpio/gpio{}/value'
GPIO_BASE_PATH_TEMPLATE = '/sys/class/gpio/gpio{}'

def is_gpio_exported(gpio_number): 
    gpio_base_path = GPIO_BASE_PATH_TEMPLATE.format(gpio_number)
    return os.path.exists(gpio_base_path)

def export_gpio(gpio_number):
    if not is_gpio_exported(gpio_number):
        try:
            with open(GPIO_EXPORT_PATH, 'w') as export_file:
                export_file.write(str(gpio_number))
        except IOError as e:
            print(f"Error exporting GPIO: {e}")
            sys.exit(1)
def unexport_gpio(gpio_number):
    try:
        with open(GPIO_UNEXPORT_PATH , 'w') as unexport_file:
            unexport_file.write(str(gpio_number))
    except IOError as e:
        print(f"Error unexporting GPIO: {e}")
        sys.exit(1)

def set_gpio_direction(gpio_number, direction):
    gpio_direction_path = GPIO_DIRECTION_PATH_TEMPLATE.format(gpio_number)
    try:
        with open(gpio_direction_path, 'w') as direction_file:
            direction_file.write(direction)
    except IOError as e:
        print(f"Error setting GPIO direction: {e}")
        sys.exit(1)

def set_gpio_value(gpio_number, value):
    gpio_value_path = GPIO_VALUE_PATH_TEMPLATE.format(gpio_number)
    try:
        with open(gpio_value_path, 'w') as value_file:
            value_file.write(str(value))
    except IOError as e:
        print(f"Error setting GPIO value: {e}")
        sys.exit(1)


## led on off 
def led_onff(gpio_number, direction, value):
    export_gpio(gpio_number)
    set_gpio_direction(gpio_number, direction)
    set_gpio_value(gpio_number, value)

## led loop 
def gpio_loop(gpio_numbers):
    while 1:
        for i in range(len(gpio_numbers)):
            led_onff(gpio_numbers[i], "out", 1)
            time.sleep(1)
            led_onff(gpio_numbers[i], "out", 0)

## led shift
def gpio_stack(gpio_numbers):
    for i in range(1,len(gpio_numbers)):
        led_onff(gpio_numbers[0], "out", 1)
        for j in range(len(gpio_numbers)-i):
            time.sleep(0.5)
            led_onff(gpio_numbers[j], "out", 0)
            led_onff(gpio_numbers[j+1], "out", 1)
        time.sleep(0.5)
    led_onff(gpio_numbers[0], "out", 1)
    time.sleep(0.5)
    for i in range(len(gpio_numbers)):
        led_onff(gpio_numbers[i], "out", 0)
    time.sleep(0.5)


if __name__ == "__main__":

    if len(sys.argv) != 4 and len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <gpio_number,...> <direction> <value>")
        print(f"Example: {sys.argv[0]} 82,83,..,87 out 1")
        print(f"Example: {sys.argv[0]} 82,83,...,87 stack")
        sys.exit(1)

    gpio_numbers = sys.argv[1].split(',')
    direction = sys.argv[2]
    if len(sys.argv) == 3:
        value = sys.argv.append("1")
    value = int(sys.argv[3])

    try:
        if direction == "out":
            for i in range(len(gpio_numbers)):
                led_onff(gpio_numbers[i], direction, value)
        elif direction == 'loop':
            gpio_loop(gpio_numbers)
        elif direction == 'stack':
            gpio_stack(gpio_numbers)
            gpio_numbers.reverse()
            gpio_stack(gpio_numbers)


    except KeyboardInterrupt:
        for i in range(len(gpio_numbers)):
            set_gpio_value(gpio_numbers[i], 0)
            unexport_gpio(gpio_numbers[i])

    sys.exit(0)