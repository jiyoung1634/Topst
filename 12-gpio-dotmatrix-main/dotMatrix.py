import sys
import os
import time

import dotsArr

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

# ROW & COL NUM
row = [115,65,112,66,118,113,120,121]
col = [84,117,83,86,114,85,90,89]

#display map
smileMap = [
    0b00111100,
    0b01000010,
    0b10100101,
    0b10000001,
    0b10100101,
    0b10011001,
    0b01000010,
    0b00111100,
]

def set_matrix_value(map):
    i = 0
    for r in map:
        set_gpio_value(row[i], 1)
        for c in range(8):
            bit = (r >> 7-c) & 0x01
            if bit == 0: set_gpio_value(col[c], 1)
            else: set_gpio_value(col[c], 0)
        turn_off_all()
        i += 1

def turn_off_all():
    for r in row:
        set_gpio_value(r,0)
    for c in col:
        set_gpio_value(c,1)


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <value>")
        sys.exit(1)

    for rowN in row:
        export_gpio(rowN)
        set_gpio_direction(rowN, "out")
    for colN in col:
        export_gpio(colN)
        set_gpio_direction(colN, "out")

    try :
        if sys.argv[1] == "smile":
            while(1):
                set_matrix_value(smileMap)
        
        if sys.argv[1] == "numbers":
            time_1 = time.time() + 1
            for i in range(len(dotsArr.numbers)):
                while(time.time() < time_1):
                    set_matrix_value(dotsArr.numbers[i])
                time_1 = time.time() + 1
        
        if sys.argv[1] == "alphabets":
            time_1 = time.time() + 1
            for i in range(len(dotsArr.alphabets)):
                while(time.time() < time_1):
                    set_matrix_value(dotsArr.alphabets[i])
                time_1 = time.time() + 1

    except Exception as e:
        turn_off_all()
    finally:
        for colN in col:
            unexport_gpio(colN)
        for rowN in row:
            unexport_gpio(rowN)

        sys.exit(0)
