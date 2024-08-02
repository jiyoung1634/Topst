from ..Library.Module import Digit_Segment_Library as digit
import time

digit_pins = [86, 85, 84, 65] # d1, d2, d3, d4
segment_pins = [112, 83, 90, 115, 117, 63, 89, 66] # a, b, c, d, e, f, g, dp

gpio_array = [
    [112,83,90,115,117,63], #0
    [83,90], #1
    [112,83,115,117,63], #2
    [112,83,90,115,63], #3
    [83,90,63,89], #4
    [112,90,115,63,89], #5
    [112,90,115,117,63,89], #6
    [112,83,90], #7
    [112,83,90,115,117,63,89], #8
    [112,83,90,115,63,89]  #9
]

if __name__ == "__main__":
        digit.set_device(segment_pins, digit_pins) # regist device
        digit.turn_off_digit(segment_pins, digit_pins)

        num = 0
        time_1 = time.time() + 1
        while(num < 10000): # display num
            digit.display(digit_pins[0], gpio_array[(num//1000)])
            digit.display(digit_pins[1], gpio_array[(num//100)%10])
            digit.display(digit_pins[2], gpio_array[(num//10)%10])
            digit.display(digit_pins[3], gpio_array[(num)%10]) 
            if time.time() > time_1:
                num += 1
                time_1 = time.time() + 1 # every second num ++
        
        digit.quit_device(segment_pins, digit_pins) # unregist device
