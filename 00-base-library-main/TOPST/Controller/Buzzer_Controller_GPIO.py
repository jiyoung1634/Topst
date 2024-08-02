from ..Library.Module import Buzzer_Library
import time
if __name__ == "__main__":

    gpio_pin = 112 # gpio pin which connected with buzzer
    second = 1 # how long turn on and off

    Buzzer_Library.set_buzzer_gpio(gpio_pin) # regist buzzer device
    
    while True:
        Buzzer_Library.turn_on_gpio(gpio_pin) # turn off buzzer
        time.sleep(second)
        Buzzer_Library.turn_off_gpio(gpio_pin) # turn off buzzer
        time.sleep(second)