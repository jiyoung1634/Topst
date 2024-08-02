from ..Library.Module import PCF8591_Library as pcf
import time

bus = 1
addr = 0x48
channel = 00
auto_increment = 0
input = 0
output = 1

if __name__ == "__main__":
    fd = pcf.open_device(bus, addr) # regist pcf8591 device
    control_byte = pcf.get_control_byte(output, input, auto_increment, channel) # get control byte
    pcf.write_device(fd, control_byte) # transfer control byte
    for i in range(10):
        print(pcf.read_device(fd, control_byte)) # read analog data
        time.sleep(0.05)
    pcf.quit_device(fd) # unregist pcf8591 device