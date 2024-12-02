import sys
import time
import RPi.GPIO as GPIO  # GPIO 라이브러리 임포트

# GPIO 핀 번호 설정 (실제 D3 보드 핀 번호로 수정 필요)
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

# 숫자별 세그먼트 배열 (각 숫자에 해당하는 세그먼트 번호를 설정)
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
    set_gpio_value(gpio_pin, 1)  # GPIO 핀을 켬

# GPIO 핀을 끄는 함수
def gpio_num_off(gpio_pin):
    set_gpio_value(gpio_pin, 0)  # GPIO 핀을 끔

# GPIO 값 설정 함수 (여기서는 예시로 출력만 합니다. 실제 GPIO 핀 제어는 라이브러리나 시스템에 맞게 설정)
def set_gpio_value(gpio_pin, value):
    if value == 1:
        print(f"GPIO Pin {gpio_pin} ON")
    else:
        print(f"GPIO Pin {gpio_pin} OFF")

# GPIO 핀 초기화
def export_gpio(gpio_pin):
    print(f"Exporting GPIO Pin {gpio_pin}")
    GPIO.setup(gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # 버튼 핀을 입력으로 설정하고 풀업 저항을 사용

# GPIO 핀 해제
def unexport_gpio(gpio_pin):
    print(f"Unexporting GPIO Pin {gpio_pin}")
    GPIO.cleanup(gpio_pin)

# GPIO 핀 방향 설정 (출력 모드로 설정)
def set_gpio_direction(gpio_pin, direction):
    print(f"Setting GPIO Pin {gpio_pin} direction to {direction}")

# 숫자 디스플레이 함수
def display_number(num):
    # num_array에서 해당 숫자에 맞는 세그먼트 번호 가져오기
    segments = num_array[num]
    
    # 모든 세그먼트 끄기
    for i in range(len(gpio)):
        gpio_num_off(gpio[i])
    
    # 해당 숫자에 맞는 세그먼트만 켜기
    for segment in segments:
        gpio_num_on(gpio[segment])

# 버튼 상태 확인 함수 (버튼을 눌렀는지 체크)
def is_button_pressed():
    return GPIO.input(button_pin) == GPIO.LOW  # 버튼을 눌렀을 때 LOW 신호가 발생

# Main 함수
if __name__ == "__main__":
    if len(sys.argv) != 1:
        print(f"Usage: {sys.argv[0]}")
        sys.exit(1)

    try:
        # GPIO 핀 초기화
        GPIO.setmode(GPIO.BCM)  # BCM 모드로 설정
        for pin in gpio:
            export_gpio(pin)
            set_gpio_direction(pin, "out")

        export_gpio(button_pin)  # 버튼 핀도 초기화

        # 숫자 변수 초기화
        num = 0
        
        while True:
            if is_button_pressed():  # 버튼이 눌리면
                num = (num + 1) % 10  # 숫자를 0부터 9까지 증가시키고, 9 이후에는 다시 0으로 돌아감
                print(f"Displaying number {num}")
                display_number(num)  # 숫자 디스플레이
                time.sleep(0.5)  # 버튼 눌림 상태가 여러 번 감지되지 않도록 잠시 대기
            time.sleep(0.1)  # 너무 자주 체크하지 않도록 약간의 지연

    except KeyboardInterrupt:
        # 사용자 중지 시 모든 GPIO 끄기
        for pin in gpio:
            gpio_num_off(pin)
    finally:
        # 종료 시 GPIO 핀 해제
        for pin in gpio:
            unexport_gpio(pin)
        GPIO.cleanup()  # GPIO 해제

    sys.exit(0)
