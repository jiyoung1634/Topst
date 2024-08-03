import sys
import os
import time

GPIO_EXPORT_PATH = "/sys/class/gpio/export"
GPIO_UNEXPORT_PATH = '/sys/class/gpio/unexport'
GPIO_DIRECTION_PATH_TEMPLATE = '/sys/class/gpio/gpio{}/direction'
GPIO_VALUE_PATH_TEMPLATE = '/sys/class/gpio/gpio{}/value'
GPIO_BASE_PATH_TEMPLATE = '/sys/class/gpio/gpio{}'



def is_gpio_exported(gpio_number): ##base path -> return T/F
    gpio_base_path = GPIO_BASE_PATH_TEMPLATE.format(gpio_number)
    return os.path.exists(gpio_base_path)

def export_gpio(gpio_number): ##BASE PATH가 존재하지 적어주기
    if not is_gpio_exported(gpio_number):
        try:
            with open(GPIO_EXPORT_PATH, 'w') as export_file:
                export_file.write(str(gpio_number))
        except IOError as e:
            print(f"Error exporting GPIO: {e}")
            sys.exit(1)
            
def unexport_gpio(gpio_number):
    try:
        with open(GPIO_UNEXPORT_PATH , 'w') as unexport_file:
            unexport_file.write(str(gpio_number))
    except IOError as e:
        print(f"Error unexporting GPIO: {e}")
        sys.exit(1)

def set_gpio_direction(gpio_number, direction):
    gpio_direction_path = GPIO_DIRECTION_PATH_TEMPLATE.format(gpio_number)
    try:
        with open(gpio_direction_path, 'w') as direction_file:
            direction_file.write(direction)
    except IOError as e:
        print(f"Error setting GPIO direction: {e}")
        sys.exit(1)

def set_gpio_value(gpio_number, value):
    gpio_value_path = GPIO_VALUE_PATH_TEMPLATE.format(gpio_number)
    try:
        with open(gpio_value_path, 'w') as value_file:
            value_file.write(str(value))
    except IOError as e:
        print(f"Error setting GPIO value: {e}")
        sys.exit(1)

#GPIO PIN NUMBER

d1 = 86
d2 = 85
d3 = 84
d4 = 65

a = 112
b = 83
c = 90
d = 115
e = 117
f = 63
g = 89
dp = 66

gpio = [a,b,c,d,e,f,g,dp,d1,d2,d3,d4]
gpio_array = [
    [a,b,c,d,e,f], #0
    [b,c], #1
    [a,b,d,e,g], #2
    [a,b,c,d,g], #3
    [b,c,f,g], #4
    [a,c,d,f,g], #5
    [a,c,d,e,f,g], #6
    [a,b,c], #7
    [a,b,c,d,e,f,g], #8
    [a,b,c,d,f,g]  #9
]

def gpio_num_on(gpio_num):
    for i in range(len(gpio_num)):
        set_gpio_value(gpio_num[i], 1)

def gpio_num_off(gpio_num):
    for i in range(len(gpio_num)):
        set_gpio_value(gpio_num[i], 0)

def gpio_digit_on(gpio_digit):
    set_gpio_value(gpio_digit, 0)

def gpio_digit_off(gpio_digit):
    set_gpio_value(gpio_digit, 1)

def gpio_turn_off():
    for i in [a,b,c,d,e,f,g,dp]:
        gpio_digit_on(i)
    for i in [d1,d2,d3,d4]:
        gpio_digit_off(i)

def display(gpio_digit, gpio_array):
    gpio_turn_off() # 모든 자리 끄기
    
    gpio_digit_on(gpio_digit)
    gpio_num_on(gpio_array)

def display_run(num):
    display(d1, gpio_array[(num//1000)])
    display(d2, gpio_array[(num//100)%10])
    display(d3, gpio_array[(num//10)%10])
    display(d4, gpio_array[(num)%10]) 

        
if __name__ == "__main__":

    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <value>")
        sys.exit(1)
    
    try:
        for i in range(len(gpio)):
            export_gpio(gpio[i])
            set_gpio_direction(gpio[i], "out")
        gpio_turn_off()

        if sys.argv[1] == "timer":
            num = 0
            time_1 = time.time() + 1
            while(num < 10000):
                display_run(num)
                if time.time() > time_1:
                    num += 1
                    time_1 = time.time() + 1

        if sys.argv[1] == "clock":
        
            while(True):
                h = time.localtime().tm_hour
                m = time.localtime().tm_min
                num = h*100+m

                display(d2,[dp])
                
                display_run(num)


        for i in [a,b,c,d,e,f,g,dp,d1,d2,d3,d4]:
            unexport_gpio(i)
        
            
    except KeyboardInterrupt:
        gpio_turn_off()
        for i in [a,b,c,d,e,f,g,dp,d1,d2,d3,d4]:
            unexport_gpio(i)       

    sys.exit(0)