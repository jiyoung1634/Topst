import RPi.GPIO as GPIO
import time

button_pin = 6  # 버튼을 연결할 GPIO 핀 번호 (실제 연결된 핀 번호로 수정 필요)

GPIO.setmode(GPIO.BOARD)  # BOARD 모드 사용
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # 버튼 핀을 입력으로 설정, 풀업 저항 활성화

try:
    while True:
        button_state = GPIO.input(button_pin)  # 버튼 상태 읽기
        print(f"Button state: {button_state}")  # 버튼 상태 출력 (0은 눌림, 1은 눌리지 않음)
        time.sleep(0.1)  # 반복문 주기

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()  # 종료 시 GPIO 핀 정리
