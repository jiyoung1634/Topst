
import sys
import os
import time

GPIO_EXPORT_PATH = "/sys/class/gpio/export"
GPIO_UNEXPORT_PATH = "/sys/class/gpio/unexport"
GPIO_DIRECTION_PATH_TEMPLATE = "/sys/class/gpio/gpio{}/direction"
GPIO_VALUE_PATH_TEMPLATE = "/sys/class/gpio/gpio{}/value"
GPIO_BASE_PATH_TEMPLATE = "/sys/class/gpio/gpio{}"

def is_gpio_exported(gpio_number):
    gpio_base_path = GPIO_BASE_PATH_TEMPLATE.format(gpio_number)
    return os.path.exists(gpio_base_path)

def export_gpio(gpio_number):
    if not is_gpio_exported(gpio_number):
        try:
            with open(GPIO_EXPORT_PATH, 'w') as export_file:
                export_file.write(str(gpio_number))
        except IOError as e:
            print(f"Error exporting GPIO {gpio_number}: {e}")
            sys.exit(1)

def unexport_gpio(gpio_number):
    try:
        with open(GPIO_UNEXPORT_PATH, 'w') as unexport_file:
            unexport_file.write(str(gpio_number))
    except IOError as e:
        print(f"Error unexporting GPIO {gpio_number}: {e}")
        sys.exit(1)

def set_gpio_direction(gpio_number, direction):
    gpio_direction_path = GPIO_DIRECTION_PATH_TEMPLATE.format(gpio_number)
    try:
        with open(gpio_direction_path, 'w') as direction_file:
            direction_file.write(direction)
    except IOError as e:
        print(f"Error setting GPIO {gpio_number} direction to {direction}: {e}")
        sys.exit(1)

def set_gpio_value(gpio_number, value):
    gpio_value_path = GPIO_VALUE_PATH_TEMPLATE.format(gpio_number)
    try:
        with open(gpio_value_path, 'w') as value_file:
            value_file.write(str(value))
    except IOError as e:
        print(f"Error setting GPIO {gpio_number} value to {value}: {e}")
        sys.exit(1)

def read_gpio_value(gpio_number):
    gpio_value_path = GPIO_VALUE_PATH_TEMPLATE.format(gpio_number)
    try:
        with open(gpio_value_path, 'r') as value_file:
            return value_file.read().strip()
    except IOError as e:
        print(f"Error reading GPIO {gpio_number} value: {e}")
        sys.exit(1)




def read_ultrasonic_sensor(trigger_pin, echo_pin, timeout=1.0):
    export_gpio(trigger_pin)
    export_gpio(echo_pin)
    set_gpio_direction(trigger_pin, "out")
    set_gpio_direction(echo_pin, "in")

    set_gpio_value(trigger_pin, 0)
    time.sleep(0.000002)  

    set_gpio_value(trigger_pin, 1)
    time.sleep(0.00001) 
    set_gpio_value(trigger_pin, 0)

    start_time = time.time()
    timeout_start = time.time()
    while read_gpio_value(echo_pin) == '0':
        if time.time() - timeout_start > timeout:
            print("Timeout waiting for echo start")
            unexport_gpio(trigger_pin)
            unexport_gpio(echo_pin)
            return None
        start_time = time.time()

    timeout_start = time.time()
    while read_gpio_value(echo_pin) == '1':
        if time.time() - timeout_start > timeout:
            print("Timeout waiting for echo end")
            unexport_gpio(trigger_pin)
            unexport_gpio(echo_pin)
            return None
        stop_time = time.time()

    elapsed_time = stop_time - start_time
    distance = (elapsed_time * 34300) / 2  

    unexport_gpio(trigger_pin)
    unexport_gpio(echo_pin)

    return distance


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <trigger_pin> <echo_pin>")
        print(f"Example: {sys.argv[0]} 65 90")
        sys.exit(1)

    try:
        trigger_pin = int(sys.argv[1])
        echo_pin = int(sys.argv[2])
    except ValueError:
        print("Invalid pin number. Pins must be integers.")
        sys.exit(1)

    try:
        while True:
            distance = read_ultrasonic_sensor(trigger_pin, echo_pin)
            if distance is not None:
                print(f"Distance: {distance:.2f} cm")
            else:
                print("Failed to measure distance")
            time.sleep(1) 
    except KeyboardInterrupt:
        unexport_gpio(trigger_pin)
        unexport_gpio(echo_pin)
        print("\nMeasurement stopped by User")
    except Exception as e:
        print(f"An error occurred: {e}")
        unexport_gpio(trigger_pin)
        unexport_gpio(echo_pin)

    sys.exit(0)
