from ..Library.Module import PCF8591_Library as pcf

def getVector(fd, x_byte, y_byte): # read data function
    x = pcf.read_device(fd, x_byte) # read axis x data
    y = pcf.read_device(fd,y_byte) # read axis y data
    return x, y

if __name__ == "__main__":
    x, y = 0, 0
    fd = pcf.open_device(1) # regist pcf8951
    axisy = pcf.get_control_byte(0,0,0,0) # read first analog register
    axisx = pcf.get_control_byte(0,0,0,1) # read second analog register
    while(True):
        x , y = getVector(fd, axisx, axisy) # get vector data
        print(f"X : {x} | Y : {y}")