
import os
import time

# GPIO path settings
GPIO_BASE_PATH = "/sys/class/gpio"
GPIO_EXPORT_PATH = os.path.join(GPIO_BASE_PATH, "export")
GPIO_UNEXPORT_PATH = os.path.join(GPIO_BASE_PATH, "unexport")

# GPIO pin condtrol functions

def gpio_export(pin):
    """Enable the GPIO pin."""
    if not os.path.exists(os.path.join(GPIO_BASE_PATH, f"gpio{pin}")):
        with open(GPIO_EXPORT_PATH, 'w') as f:
            f.write(str(pin))

def gpio_unexport(pin):
    """Enable the GPIO pin."""
    with open(GPIO_UNEXPORT_PATH, 'w') as f:
        f.write(str(pin))

def gpio_set_direction(pin, direction):
    """Sets the direction of the GPIO pin."""
    direction_path = os.path.join(GPIO_BASE_PATH, f"gpio{pin}", "direction")
    with open(direction_path, 'w') as f:
        f.write(direction)

def gpio_write(pin, value):
    """Write the value on the GPIO pin."""
    value_path = os.path.join(GPIO_BASE_PATH, f"gpio{pin}", "value")
    with open(value_path, 'w') as f:
        f.write(str(value))

def gpio_read(pin):
    """Read the value on the GPIO pin."""
    value_path = os.path.join(GPIO_BASE_PATH, f"gpio{pin}", "value")
    with open(value_path, 'r') as f:
        return f.read().strip()

# pin number setting (BCM) mode
PIR_SENSOR_PIN = 86  # PIR sensor
LED_PIN = 84         # LED 

# GPIO pin activate / setting
gpio_export(PIR_SENSOR_PIN)
gpio_export(LED_PIN)
gpio_set_direction(PIR_SENSOR_PIN, "in")
gpio_set_direction(LED_PIN, "out")

def read_pir_sensor(pin, samples=10, interval=0.05):
    """Returns the average by reading the sample multiple times from the PIR sensor."""
    readings = []
    for _ in range(samples):
        readings.append(int(gpio_read(pin)))
        time.sleep(interval)
    return sum(readings) / samples

try:
    while True:
        pir_value = read_pir_sensor(PIR_SENSOR_PIN)
        if pir_value >= 0.5:  # If the mean value is greater than 0.5, it is determined as motion detection
            gpio_write(LED_PIN, 1)  # LED ON
            print("Motion detected!")
        else:
            gpio_write(LED_PIN, 0)  # LED OFF
            print("Motion NOT detected!")
        time.sleep(0.5)  # Periodic delay (recurring cycle adjustable)
except KeyboardInterrupt:
    print("Program terminated")
finally:
    gpio_unexport(PIR_SENSOR_PIN)
    gpio_unexport(LED_PIN)