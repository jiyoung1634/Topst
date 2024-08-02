from .. import GPIO_Library as gpio
import time

# set device for use device
def set_device(echo_pin, trigger_pin):
    gpio.export(echo_pin)
    gpio.set_direction(echo_pin, "in")
    gpio.export(trigger_pin)
    gpio.set_direction(trigger_pin, "out")

# read distance by device
def read_distance(echo_pin, trigger_pin, timeout = 0.05):
    gpio.set_value(trigger_pin, 0) # start trigger signal
    time.sleep(0.000001)
    gpio.set_value(trigger_pin, 1) # send trigger signal
    time.sleep(0.00001)
    gpio.set_value(trigger_pin, 0) # wait for signal
    time.sleep(0.0002)
    return measure_distance(echo_pin, timeout)

def measure_distance(echo_pin, timeout):
    start = time.time()
    timeout_start = time.time()
    while gpio.get_value(echo_pin) == '0': #wait for get signal by echo_pin
        if time.time() - timeout_start > timeout:
            return None
        start = time.time()
    
    timeout_start = time.time()
    while gpio.get_value(echo_pin) == '1': #time check for measure how long
        if time.time() - timeout_start > timeout:
            return None 
        stop = time.time()
    time.sleep(0.01)
    eslapse = stop - start # calculate eslapsed time
    return eslapse * 34300 / 2  # calculate distance by eslapsed time

# quit device after using device
def disable_device(echo_pin, trigger_pin):
    gpio.unexport(echo_pin)
    gpio.unexport(trigger_pin)