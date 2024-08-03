import sys
import os
import time

GPIO_EXPORT_PATH = "/sys/class/gpio/export"
GPIO_UNEXPORT_PATH = '/sys/class/gpio/unexport'
GPIO_DIRECTION_PATH_TEMPLATE = '/sys/class/gpio/gpio{}/direction'
GPIO_VALUE_PATH_TEMPLATE = '/sys/class/gpio/gpio{}/value'
GPIO_BASE_PATH_TEMPLATE = '/sys/class/gpio/gpio{}'

def is_gpio_exported(gpio_number): ##base path -> return T/F
    gpio_base_path = GPIO_BASE_PATH_TEMPLATE.format(gpio_number)
    return os.path.exists(gpio_base_path)

def export_gpio(gpio_number): ##BASE PATH가 존재하지 적어주기
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

#GPIO PIN NUMBER
a = 81
b = 82
c = 89
d = 88
e = 87
f = 83
g = 84
dp = 90

gpio = [a,b,c,d,e,f,g,dp]
gpio_array = [
    [a,b,c,d,e,f], #0
    [b,c], #1
    [a,b,d,e,g], #2
    [a,b,c,d,g], #3
    [b,c,f,g], #4
    [a,c,d,f,g], #5
    [a,c,d,e,f,g], #6
    [a,b,c], #7
    [a,b,c,d,e,f,g], #8
    [a,b,c,d,f,g]  #9
]

def gpio_num_on(gpio_num):
    for i in range(len(gpio_num)):
        set_gpio_value(gpio_num[i], 1)

def gpio_num_off(gpio_num):
    for i in range(len(gpio_num)):
        set_gpio_value(gpio_num[i], 0)

if __name__ == "__main__":

    if len(sys.argv) != 1:
        print(f"Usage: {sys.argv[0]}")
        sys.exit(1)

    try:
        for i in range(len(gpio)):
            export_gpio(gpio[i])
            set_gpio_direction(gpio[i], "out")

        for i in range(len(gpio_array)):
            gpio_num_on(gpio_array[i])
            time.sleep(1)
            gpio_num_off(gpio_array[i])          
        
    except KeyboardInterrupt:
        for i in range(len(gpio_array)):
            gpio_num_off(gpio_array[i])
    finally:
        for i in range(len(gpio)):
            unexport_gpio(gpio[i])

    sys.exit(0)