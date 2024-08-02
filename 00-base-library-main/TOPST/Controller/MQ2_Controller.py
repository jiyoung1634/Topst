from ..Library.Module import PCF8591_Library as pcf
from ..Library.Module import MQ2_Library as mq2
import time

bus = 1
addr = 0x48
channel = 00
auto_increment = 0
input = 0
output = 1
gpio_pin = 84

if __name__ == "__main__":
    fd = pcf.open_device(bus, addr) # regist pcf8591
    mq2.set_device(gpio_pin) # regist mq2 digital output
    control_byte = pcf.get_control_byte(output, input, auto_increment, channel) # get control byte -> read first analog register
    pcf.write_device(fd, control_byte) # transfer control byte
    for i in range(10):
        print(pcf.read_device(fd, control_byte)) # read analog data and print
        print(mq2.get_value(gpio_pin)) # read digital data and print
        time.sleep(0.05)
    pcf.quit_device(fd) # unregist pcf8591
    mq2.quit_device(gpio_pin) # unregist digital output