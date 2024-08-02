from ..Library.Module import RGB_Led_Library as rgb

rgb_pins = [112,113,114] # red, green, blue gpio pin
values = [0,1,1] # green + blue => yellow

if __name__ == "__main__":
    rgb.set_device(rgb_pins) # regist device
    rgb.set_value(rgb_pins, values) # turn on yellow light
    rgb.set_value(rgb_pins, [0,0,0]) # turn off
    rgb.quit_device(rgb_pins) # unregist device