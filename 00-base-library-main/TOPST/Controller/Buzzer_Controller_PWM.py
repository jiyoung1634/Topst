from ..Library.Module import Buzzer_Library

if __name__ == "__main__":
    
    gpio_pin = 112
    channel = 2
    hz = 3

    Buzzer_Library.set_buzzer_pwm(channel) # regist buzzer pwm channel
    Buzzer_Library.turn_on_pwm(channel) # pwm signal enable
    while True:
        Buzzer_Library.set_tone_pwm(channel, hz) # set pwm signal hz
        if(input(hz)=="q"):
            Buzzer_Library.turn_off_pwm(channel) # turn off buzzer
        else:
            Buzzer_Library.turn_on_gpio(channel) # turn on buzzer