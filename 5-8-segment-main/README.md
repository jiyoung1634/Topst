import sys
import time
import RPi.GPIO as GPIO

# GPIO 핀 번호 설정
a = 81
b = 82
c = 89
d = 88
e = 87
f = 83
g = 84
dp = 90

# GPIO 핀 배열
gpio = [a, b, c, d, e, f, g, dp]

# 숫자별 세그먼트 배열
num_array = [
    [0, 1, 2, 3, 4, 5], 
    [1, 2],                 
    [0, 1, 3, 4, 6],        
    [0, 1, 2, 3, 6],        
    [1, 2, 5, 6],           
    [0, 2, 3, 5, 6],        
    [0, 2, 3, 4, 5, 6],     
    [0, 1, 2],              
    [0, 1, 2, 3, 4, 5, 6],  
    [0, 1, 2, 3, 5, 6]      
]

# GPIO 핀을 켜는 함수
def gpio_num_on(gpio_pin):
    GPIO.output(gpio_pin, GPIO.HIGH)

# GPIO 핀을 끄는 함수
def gpio_num_off(gpio_pin):
    GPIO.output(gpio_pin, GPIO.LOW)

# GPIO 값 설정 함수
def set_gpio_value(gpio_pin, value):
    if value == 1:
        gpio_num_on(gpio_pin)
    else:
        gpio_num_off(gpio_pin)

# 숫자 디스플레이 함수
def display_number(num):
    segments = num_array[num]
    
    # 모든 세그먼트 끄기
    for i in range(len(gpio)):
        gpio_num_off(gpio[i])
    
    # 해당 숫자에 맞는 세그먼트만 켜기
    for segment in segments:
        gpio_num_on(gpio[segment])

# Main 함수
if __name__ == "__main__":
    if len(sys.argv) != 1:
        print(f"Usage: {sys.argv[0]}")
        sys.exit(1)

    try:
        GPIO.setmode(GPIO.BCM)  # BCM 핀 번호 사용
        for pin in gpio:
            GPIO.setup(pin, GPIO.OUT)

        # 숫자 표시
        for num in range(10):
            print(f"Displaying number {num}")
            display_number(num)
            time.sleep(1)

    except KeyboardInterrupt:
        # 사용자 중지 시 모든 GPIO 끄기
        for pin in gpio:
            gpio_num_off(pin)
    finally:
        # 종료 시 GPIO 핀 해제
        GPIO.cleanup()

    sys.exit(0)
