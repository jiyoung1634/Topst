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

button_gpio = 89  
buzzer_gpio = 90  

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
            return value_file.read().strip()
    except IOError as e:
        print(f"Error getting GPIO value: {e}")
        sys.exit(1)

# Signal handler to cleanup on exit
def signal_handler(sig, frame):
    unexport_gpio(button_gpio)
    unexport_gpio(buzzer_gpio)
    sys.exit(0)

# Register the signal handler for cleanup
signal.signal(signal.SIGINT, signal_handler)

# Export and configure GPIOs
export_gpio(button_gpio)
export_gpio(buzzer_gpio)
set_gpio_direction(button_gpio, 'in')
set_gpio_direction(buzzer_gpio, 'out')

try:
    while True:
        button_state = get_gpio_value(button_gpio)
        if button_state == '0':  
            set_gpio_value(buzzer_gpio, 0)  
            print("Button not pressed, buzzer off")
        else:
            set_gpio_value(buzzer_gpio, 1)  
            print("Button pressed, buzzer on")
        time.sleep(0.1)

except KeyboardInterrupt:
    signal_handler(signal.SIGINT, None)