import RPi.GPIO as GPIO
import time

button_pin = 6  # 버튼을 연결할 GPIO 핀 번호
gpio = [81, 82, 89, 88, 87, 83, 84, 90]  # 세그먼트 디스플레이 GPIO 핀
num_array = [
    [0, 1, 2, 3, 4, 5],       # 0
    [1, 2],                   # 1
    [0, 1, 3, 4, 6],          # 2
    [0, 1, 2, 3, 6],          # 3
    [1, 2, 5, 6],             # 4
    [0, 2, 3, 5, 6],          # 5
    [0, 2, 3, 4, 5, 6],       # 6
    [0, 1, 2],                # 7
    [0, 1, 2, 3, 4, 5, 6],    # 8
    [0, 1, 2, 3, 5, 6]        # 9
]

# 세그먼트 디스플레이 ON/OFF
def gpio_num_on(gpio_pin):
    set_gpio_value(gpio_pin, 1)

def gpio_num_off(gpio_pin):
    set_gpio_value(gpio_pin, 0)

def set_gpio_value(gpio_pin, value):
    if value == 1:
        print(f"GPIO Pin {gpio_pin} ON")
    else:
        print(f"GPIO Pin {gpio_pin} OFF")

def display_number(num):
    segments = num_array[num]
    for i in range(len(gpio)):
        gpio_num_off(gpio[i])  # 모든 세그먼트 끄기
    for segment in segments:
        gpio_num_on(gpio[segment])  # 해당 세그먼트만 켜기

# GPIO 설정
GPIO.setmode(GPIO.BOARD)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # 풀업 저항 활성화

# 버튼 눌렀을 때만 숫자 증가하도록 설정
current_number = 0

try:
    while True:
        button_state = GPIO.input(button_pin)  # 버튼 상태 읽기
        if button_state == GPIO.LOW:  # 버튼 눌렸을 때
            print("Button Pressed")
            current_number += 1
            if current_number > 9:
                current_number = 0  # 9에서 다시 0으로 순환
            display_number(current_number)  # 숫자 디스플레이
            time.sleep(0.3)  # 디바운싱을 위한 대기 시간 추가
        else:
            print("Button Released")
        time.sleep(0.1)  # 반복문 주기

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()  # 종료 시 GPIO 핀 정리
