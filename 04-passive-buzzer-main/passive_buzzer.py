import sys
import os
import time
import Cangeroo  # Cangeroo 라이브러리 임포트

# GPIO 핀 설정
GPIO_EXPORT_PATH = "/sys/class/gpio/export"
GPIO_UNEXPORT_PATH = "/sys/class/gpio/unexport"
GPIO_DIRECTION_PATH_TEMPLATE = "/sys/class/gpio/gpio{}/direction"
GPIO_VALUE_PATH_TEMPLATE = "/sys/class/gpio/gpio{}/value"
GPIO_BASE_PATH_TEMPLATE = "/sys/class/gpio/gpio{}"

# 음계 주파수 정의
FREQUENCIES = {
    'C': 261.63,  # 도
    'D': 293.66,  # 레
    'E': 329.63,  # 미
    'F': 349.23,  # 파
    'G': 392.00,  # 솔
    'A': 440.00,  # 라
    'B': 493.88,  # 시
    'C5': 523.25  # 높은 도
}

def is_gpio_exported(gpio_number):
    gpio_base_path = GPIO_BASE_PATH_TEMPLATE.format(gpio_number)
    return os.path.exists(gpio_base_path)

def export_gpio(gpio_number):
    if not is_gpio_exported(gpio_number):
        try:
            with open(GPIO_EXPORT_PATH, 'w') as export_file:
                export_file.write(str(gpio_number))
        except IOError as e:
            print(f"Error exporting GPIO {gpio_number}: {e}")
            sys.exit(1)

def unexport_gpio(gpio_number):
    try:
        with open(GPIO_UNEXPORT_PATH, 'w') as unexport_file:
            unexport_file.write(str(gpio_number))
    except IOError as e:
        print(f"Error unexporting GPIO {gpio_number}: {e}")
        sys.exit(1)

def set_gpio_direction(gpio_number, direction):
    gpio_direction_path = GPIO_DIRECTION_PATH_TEMPLATE.format(gpio_number)
    try:
        with open(gpio_direction_path, 'w') as direction_file:
            direction_file.write(direction)
    except IOError as e:
        print(f"Error setting GPIO {gpio_number} direction to {direction}: {e}")
        sys.exit(1)

def set_gpio_value(gpio_number, value):
    gpio_value_path = GPIO_VALUE_PATH_TEMPLATE.format(gpio_number)
    try:
        with open(gpio_value_path, 'w') as value_file:
            value_file.write(str(value))
    except IOError as e:
        print(f"Error setting GPIO {gpio_number} value to {value}: {e}")
        sys.exit(1)

def play_tone(gpio_number, frequency, duration):
    period = 1.0 / frequency
    half_period = period / 2
    end_time = time.time() + duration

    while time.time() < end_time:
        set_gpio_value(gpio_number, 1)
        time.sleep(half_period)
        set_gpio_value(gpio_number, 0)
        time.sleep(half_period)

# CAN 메시지 수신 후 버저 음 출력
def can_message_received(data):
    # 수신한 CAN 데이터가 음계 값에 해당하면 버저에서 소리 출력
    note_map = {
        1: 'C',  # 1 -> 도
        2: 'D',  # 2 -> 레
        3: 'E',  # 3 -> 미
        4: 'F',  # 4 -> 파
        5: 'G',  # 5 -> 솔
        6: 'A',  # 6 -> 라
        7: 'B',  # 7 -> 시
        8: 'C5'  # 8 -> 높은 도
    }

    if data in note_map:
        note = note_map[data]
        frequency = FREQUENCIES[note]
        print(f"Playing {note} at {frequency} Hz")
        play_tone(89, frequency, 0.5)  # GPIO 89번 핀에서 음 출력

# Cangeroo를 통해 CAN 메시지를 수신
def start_can_listener():
    Cangeroo.set_callback(can_message_received)  # 수신한 메시지 처리 함수 등록
    Cangeroo.start_receiving()  # CAN 메시지 수신 시작

def main():
    gpio_pin = 89  # 버저가 연결된 GPIO 핀 번호

    try:
        export_gpio(gpio_pin)
        set_gpio_direction(gpio_pin, "out")

        # CAN 메시지 수신 시작
        start_can_listener()

        # CAN 메시지 대기
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n프로그램이 종료되었습니다.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        unexport_gpio(gpio_pin)

if __name__ == "__main__":
    main()
