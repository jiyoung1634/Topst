from ..Library.Module import Segment_Library as segment

# connected segment gpio pins
gpio_pins = [81,82,89,88,87,83,84,90]

# data => display 9
data = [81,82,89,88,83,84]

if __name__ == "__main__":
    segment.set_device(gpio_pins) # regist device
    for i in range(9):
        segment.display_num(gpio_pins, i) # display number 0~8
    segment.display_on(data) # display number 9

    segment.quit_device(gpio_pins) # unregist device