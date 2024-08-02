from ..Library.Module import HC_SR04_Library as hc

echo = 112
trig = 113

if __name__ == "__main__":
    hc.set_device(echo, trig) # regist hc-sr04
    print(hc.read_distance(echo, trig)) # read data from hc-sr04
    hc.disable_device(echo, trig) # unregist hc-sr04