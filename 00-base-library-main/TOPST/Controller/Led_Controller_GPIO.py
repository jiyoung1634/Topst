from ..Library.Module import Led_Library
import time

if __name__ == "__main__":
    gpio_pin = 112
    second = 1

    Led_Library.set_led_gpio(gpio_pin) # regist gpio pin
    while True:
        Led_Library.turn_on_gpio(gpio_pin) # turn on led
        time.sleep(int(second))
        Led_Library.turn_off_gpio(gpio_pin) # turn off led
        time.sleep(int(second))
        if(KeyboardInterrupt):
            Led_Library.quit_led_gpio(gpio_pin) # unregist gpio pin
            break