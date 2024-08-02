import os
import sys
import fcntl

device_path = "/dev/i2c-{}" #i2c device bus path
i2c_slave = 0x0703 #i2c slave set constant

# open i2c bus which we use
def i2c_open(bus):
    try:
        fd = os.open(device_path.format(bus), os.O_RDWR)
    except FileNotFoundError:
        print(f"Error : i2c_open : i2c device file not found")
        sys.exit(1)
    return fd

# set slave device, connect with i2c communication
# addr : i2c connected device's address (i2cdetect function can show address where connected with device)
def i2c_set_slave(fd, addr):
    try:
        fcntl.ioctl(fd, i2c_slave, addr) #i2c_slave is a constant which definition at device's data sheet or fcntl library
    except IOError as e:
        print(f"Error : Setting I2C Address {addr}: {e}")
        sys.exit(1)

# read function when need to select i2c device's register
# length's unit is device
def i2c_read_reg(fd, reg, length):
    try:
        i2c_write(fd, reg)
        return os.read(fd, length)
    except IOError as e:
        print(f"Error : I2C Device Reading Register {reg} : {e}")
        sys.exit(1)

# read function when unnecessary to select i2c device's register
# length's unit is device
def i2c_read(fd, length):
    try:
        return os.read(fd, length)
    except IOError as e:
        print(f"Error : I2C Device Reading Register : {e}")
        sys.exit(1)

# write function when need to select i2c device's register
def i2c_write_reg(fd, reg, data):
    try:
        os.write(fd, bytes([reg]+data))
    except IOError as e:
        print(f"Error : I2C Device Writing Register {reg} : {e}")
        sys.exit(1)

# write function when unnecessary to select i2c device's register
def i2c_write(fd, data):
    try:
        os.write(fd, bytes([data]))
    except IOError as e:
        print(f"Error : I2C Device Writing Register : {e}") 
        sys.exit(1)

# close file descriptor after use i2c device
def i2c_quit(fd):
    os.close(fd)