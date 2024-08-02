from .. import I2C_Library as i2c

# set i2c bus and device address (default address : 0x48)
def open_device(bus, addr = 0x48):
    fd = i2c.i2c_open(bus)
    i2c.i2c_set_slave(fd, addr)
    return fd

# output : enable output, input : method of get value, auto_increment, channel : analog register number (0~3)
# get control byte for control pcf8591 device
def get_control_byte(output, input, auto_increment, channel):
    control_byte = str(0)
    control_byte = control_byte + str(output)
    control_byte = control_byte + int_to_binary_string(input)
    control_byte = control_byte + str(0)
    control_byte = control_byte + str(auto_increment)
    control_byte = control_byte + int_to_binary_string(channel)

    print(control_byte)
    return int(control_byte, 2)

# make int to binary string
def int_to_binary_string(bit_value):
    binary_string = bin(bit_value)[2:]
    if len(binary_string) == 1:
        binary_string = '0' + binary_string
    return binary_string

# transfer control byte
def write_device(fd, control_byte):
    i2c.i2c_write(fd, control_byte)

# get value from pcf8591
def read_device(fd, control_byte):
    i2c.i2c_write(fd, control_byte)
    while(True):
        data = i2c.i2c_read(fd, 2)[1]
        if(data!= 128):
            break
    return data

# quit i2c communication after using device
def quit_device(fd):
    i2c.i2c_quit(fd)