from ..Library.Module import Led_Library
import time

if __name__ == "__main__":
    
    channel = 2
    second = 3
    cycle = 1

    Led_Library.set_led_pwm(channel) # regist pwm channel
    Led_Library.set_led_cycle(channel, second, cycle) # set  led pulse cycle
    while True:
        Led_Library.turn_on_pwm(channel) # turn on led
        time.sleep(1)