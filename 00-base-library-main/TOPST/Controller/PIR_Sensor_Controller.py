from ..Library.Module import PIR_Sensor_Library as pir

gpio_pin = 86
cnt = 0

if __name__ == "__main__":
    pir.set_device(gpio_pin) # regist device
    while(cnt < 10000): 
        print(pir.read_data(gpio_pin)) # print read data
        cnt += 1
    pir.quit_device(gpio_pin) # unregist device