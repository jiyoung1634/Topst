
import sys
import os
import time
import signal

# Define paths for GPIO operations
GPIO_EXPORT_PATH = "/sys/class/gpio/export"
GPIO_UNEXPORT_PATH = '/sys/class/gpio/unexport'
GPIO_DIRECTION_PATH_TEMPLATE = '/sys/class/gpio/gpio{}/direction'
GPIO_VALUE_PATH_TEMPLATE = '/sys/class/gpio/gpio{}/value'
GPIO_BASE_PATH_TEMPLATE = '/sys/class/gpio/gpio{}'

# Check if the GPIO is already exported by verifying the base path
def is_gpio_exported(gpio_number):
    gpio_base_path = GPIO_BASE_PATH_TEMPLATE.format(gpio_number)
    return os.path.exists(gpio_base_path)

# Export the GPIO if the base path does not exist
def export_gpio(gpio_number):
    if not is_gpio_exported(gpio_number):
        try:
            with open(GPIO_EXPORT_PATH, 'w') as export_file:
                export_file.write(str(gpio_number))
        except IOError as e:
            print(f"Error exporting GPIO: {e}")
            sys.exit(1)

# Unexport the GPIO
def unexport_gpio(gpio_number):
    if is_gpio_exported(gpio_number):
        try:
            with open(GPIO_UNEXPORT_PATH, 'w') as unexport_file:
                unexport_file.write(str(gpio_number))
        except IOError as e:
            print(f"Error unexporting GPIO: {e}")
            sys.exit(1)

# Set the direction of the GPIO (e.g., 'in' or 'out')
def set_gpio_direction(gpio_number, direction):
    gpio_direction_path = GPIO_DIRECTION_PATH_TEMPLATE.format(gpio_number)
    try:
        with open(gpio_direction_path, 'w') as direction_file:
            direction_file.write(direction)
    except IOError as e:
        print(f"Error setting GPIO direction: {e}")
        sys.exit(1)

# Set the value of the GPIO (e.g., 1 or 0)
def set_gpio_value(gpio_number, value):
    gpio_value_path = GPIO_VALUE_PATH_TEMPLATE.format(gpio_number)
    try:
        with open(gpio_value_path, 'w') as value_file:
            value_file.write(str(value))
    except IOError as e:
        print(f"Error setting GPIO value: {e}")
        sys.exit(1)

# Get the value of the GPIO (e.g., 1 or 0)
def get_gpio_value(gpio_number):
    gpio_value_path = GPIO_VALUE_PATH_TEMPLATE.format(gpio_number)
    try:
        with open(gpio_value_path, 'r') as value_file:
            return int(value_file.read().strip())
    except IOError as e:
        print(f"Error getting GPIO value: {e}")
        sys.exit(1)

# GPIO pin reset
def initialize_gpio(gpio_number, direction):
    unexport_gpio(gpio_number)
    export_gpio(gpio_number)
    set_gpio_direction(gpio_number, direction)

# motor control function
def motor_control(in1, in2, enable, direction, pwm):
    if direction == "forward":
        set_gpio_value(in1, 1)
        set_gpio_value(in2, 0)
    else:  # stop
        set_gpio_value(in1, 0)
        set_gpio_value(in2, 0)
    
    set_gpio_value(enable, pwm)

# Main code starts here
if __name__ == "__main__":


    IN1 = 121
    IN2 = 117
    ENABLE = 114
    BUTTON_PIN = 90
    LED_PIN = 65


    # GPIO pin reset
    initialize_gpio(IN1, 'out')
    initialize_gpio(IN2, 'out')
    initialize_gpio(ENABLE, 'out')
    initialize_gpio(BUTTON_PIN, 'in')
    initialize_gpio(LED_PIN, 'out')

    # initial, led & motor off
    set_gpio_value(LED_PIN, 1)
    motor_control(IN1, IN2, ENABLE, "stop", 0)

    motor_running = False

    try:
        while True:
            button_state = get_gpio_value(BUTTON_PIN)
            if button_state == 1:  # button on
                if not motor_running:
                    # motor forward & LED ON
                    motor_control(IN1, IN2, ENABLE, "forward", 1)
                    set_gpio_value(LED_PIN, 0)
                    motor_running = True
                else:
                    # MOTOR STOP & LED OFF
                    motor_control(IN1, IN2, ENABLE, "stop", 0)
                    set_gpio_value(LED_PIN, 1)
                    motor_running = False
                time.sleep(0.5)  # Debounce delay
            time.sleep(0.1)  # Polling delay
    except KeyboardInterrupt:
        print("Terminated by Keyboard Interrupt")
        motor_control(IN1, IN2, ENABLE, "stop", 0)
        set_gpio_value(LED_PIN, 0)
        for gpio in [IN1, IN2, ENABLE, BUTTON_PIN, LED_PIN]:
            unexport_gpio(gpio)
