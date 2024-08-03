import sys
import os
import time

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

# Function to turn LED on or off
def led_onoff(gpio_number, direction, value):
    export_gpio(gpio_number)
    set_gpio_direction(gpio_number, direction)
    set_gpio_value(gpio_number, value)

# RGB LED function
def set_rgb_led(red_pin, green_pin, blue_pin, red_value, green_value, blue_value):
    led_onoff(red_pin, 'out', red_value)
    led_onoff(green_pin, 'out', green_value)
    led_onoff(blue_pin, 'out', blue_value)

# Main code starts here
if __name__ == "__main__":

    RED_PIN = 84
    GREEN_PIN = 85
    BLUE_PIN = 89

    try:
        while True:
            set_rgb_led(RED_PIN, GREEN_PIN, BLUE_PIN, 1, 0, 0)  # red
            time.sleep(1)
            set_rgb_led(RED_PIN, GREEN_PIN, BLUE_PIN, 0, 1, 0)  # green
            time.sleep(1)
            set_rgb_led(RED_PIN, GREEN_PIN, BLUE_PIN, 0, 0, 1)  # blue
            time.sleep(1)
            set_rgb_led(RED_PIN, GREEN_PIN, BLUE_PIN, 1, 1, 0)  # yellow
            time.sleep(1)
            set_rgb_led(RED_PIN, GREEN_PIN, BLUE_PIN, 0, 1, 1)  # bluish green
            time.sleep(1)
            set_rgb_led(RED_PIN, GREEN_PIN, BLUE_PIN, 1, 0, 1)  # magenta
            time.sleep(1)
            set_rgb_led(RED_PIN, GREEN_PIN, BLUE_PIN, 0, 0, 0)  # off
            time.sleep(1)
    except KeyboardInterrupt:
        set_rgb_led(RED_PIN, GREEN_PIN, BLUE_PIN, 0, 0, 0)
        unexport_gpio(RED_PIN)
        unexport_gpio(GREEN_PIN)
        unexport_gpio(BLUE_PIN)

    print("RGB LED Control Finished")
    sys.exit(0)