import sys
import time
import RPi.GPIO as GPIO  # GPIO 라이브러리 임포트

# GPIO 핀 번호 설정
a = 81  # GPIO Pin for segment A
b = 82  # GPIO Pin for segment B
c = 89  # GPIO Pin for segment C
d = 88  # GPIO Pin for segment D
e = 87  # GPIO Pin for segment E
f = 83  # GPIO Pin for segment F
g = 84  # GPIO Pin for segment G
dp = 90  # GPIO Pin for Decimal Point
button_pin = 6  # 버튼 GPIO 핀 (GPIO6으로 수정)

# GPIO 핀 배열
gpio = [a, b, c, d, e, f, g, dp]

# 숫자별 세그먼트 배열
num_array = [
    [0, 1, 2, 3, 4, 5],       # 숫자 0
    [1, 2],                   # 숫자 1
    [0, 1, 3, 4, 6],          # 숫자 2
    [0, 1, 2, 3, 6],          # 숫자 3
    [1, 2, 5, 6],             # 숫자 4
    [0, 2, 3, 5, 6],          # 숫자 5
    [0, 2, 3, 4, 5, 6],       # 숫자 6
    [0, 1, 2],                # 숫자 7
    [0, 1, 2, 3, 4, 5, 6],    # 숫자 8
    [0, 1, 2, 3, 5, 6]        # 숫자 9
]

# GPIO 핀을 켜는 함수
def gpio_num_on(gpio_pin):
    set_gpio_value(gpio_pin, 1)

# GPIO 핀을 끄는 함수
def gpio_num_off(gpio_pin):
    set_gpio_value(gpio_pin, 0)

# GPIO 값 설정 함수
def set_gpio_value(gpio_pin, value):
    if value == 1:
        print(f"GPIO Pin {gpio_pin} ON")
    else:
        print(f"GPIO Pin {gpio_pin} OFF")

# 숫자 디스플레이 함수
def display_number(num):
    print(f"Displaying number: {num}")  # 숫자가 변경될 때마다 출력 (디버깅 용)
    segments = num_array[num]
    
    # 모든 세그먼트 끄기
    for i in range(len(gpio)):
        gpio_num_off(gpio[i])
    
    # 해당 숫자에 맞는 세그먼트만 켜기
    for segment in segments:
        gpio_num_on(gpio[segment])

# 버튼 상태 확인 함수
def is_button_pressed():
    state = GPIO.input(button_pin)
    print(f"Button state: {state}")  # 버튼 상태 출력 (디버깅 용)
    return state == GPIO.LOW  # 버튼을 눌렀을 때 LOW 신호가 발생

# Main 함수
if __name__ == "__main__":
    if len(sys.argv) != 1:
        print(f"Usage: {sys.argv[0]}")
        sys.exit(1)

    try:
        # GPIO 핀 초기화
        GPIO.setmode(GPIO.BCM)
        for pin in gpio:
            GPIO.setup(pin, GPIO.OUT)
        GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        num = 0

        while True:
            if is_button_pressed():  # 버튼이 눌리면
                num = (num + 1) % 10  # 숫자 증가
                display_number(num)  # 숫자 디스플레이
                time.sleep(0.5)  # 버튼 눌림 상태가 여러 번 감지되지 않도록 잠시 대기
            time.sleep(0.1)  # 너무 자주 체크하지 않도록 약간의 지연

    except KeyboardInterrupt:
        for pin in gpio:
            gpio_num_off(pin)
    finally:
        GPIO.cleanup()  # 종료 시 GPIO 해제

    sys.exit(0)
