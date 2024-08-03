# TOPST D3_ Gas Sensor Controller

## Introduction

In this document, we'll control a Gas Sensor
<br>
<br>
**1. Detected Gas**
    : It detects gas and displays the results in number using the D3 board and Gas Sensor
<br>

The **method** is to **use libraries**. Libraries allow you to operate components more conveniently<br>

Additionally,<Br>
You can find Library at 00_Base_Library Documentary. When you want to learn more deeply reference them.


## Materials
|DEVICE|MODEL NAME|NUM|
|:------:|:------:|:------:|
|TOPST BOARD|D3|1|
|Gas Sensor||1|
|PCF8591||1|
|GPIO Extention Board||1|
|WIRE|||


## Circuit Picture
<p align="center">
<img src="image/gassensor.jpg" width="500" height="500" >
</p>
<p align="center">
<img src="image/circuit.png" width="400" height="600" >
<br> 

### D3 BOARD

|PIN Number|PIN Name|Opponent's PIN|Connect Device|
|:------:|:------:|:------:|------|
|2|5V0|VCC|PCF8591|
|3|GPIO82|SDA|PCF8591|
|5|GPIO81|SCL|PCF8591|
|6|GND|GND|PCF8591|

### Gas Sensor

|PIN Number|PIN Name|Opponent's PIN|Connect Device|
|:------:|:------:|:------:|------|
|VCC|Gas Sensor|VCC|PCF8591|
|GND|Gas Sensor|GND|PCF8591|
|D0|Gas Sensor|IN0|PCF8591|


The negative (-) side of the resistor is connected to the ground, <br>
and the positive (+) side is connected to the GPIO pin.

## GPIO Pin Map
<br>

<p align="center">
<img src="image/PINMAP.png" width="500" height="400" >


<BR>

## 1. Code_ Gas Sensor
### Code When using libraries
- MQ2 Library
```python
from .. import GPIO_Library as gpio

# set gpio pin for use device
def set_device(gpio_pin):
    gpio.export(gpio_pin)
    gpio.set_direction(gpio_pin, "in")

# get value from device
def get_value(gpio_pin):
    value = gpio.get_value(gpio_pin)
    if value == 1:
        return True
    else:
        return False

def quit_device(gpio_pin):
    gpio.unexport(gpio_pin)
```
- PCF8591 Library
```python
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
```
- Controller
```python
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
```
**To run this script, you would use:**

Be sure to download script file at **00_Base_Library**.

Location of scripts can cause error.

When you write script yourself, modify **import path**.

```
cd {parent directory path which can include library and controller both}
python3 -m {controller script path}
```

For example:
```
cd TOPST
python3 -m TOPST.Controller.MQ2_Controller
```
<br>

## Result Mov

- Gas Sensor<br>
![Alt text](image/gassensor.mp4)

