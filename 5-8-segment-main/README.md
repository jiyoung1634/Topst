import RPi.GPIO as GPIO
import time

button_pin = 5  # 버튼을 연결할 GPIO 핀 번호 (핀 번호가 맞는지 확인)

GPIO.setmode(GPIO.BOARD)  # BOARD 모드 사용
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # 버튼 핀을 입력으로 설정, 풀업 저항 활성화

try:
    while True:
        # GPIO 상태 출력
        button_state = GPIO.input(button_pin)
        print(f"GPIO {button_pin} state: {button_state}")  # GPIO 상태 출력 (LOW면 눌림)

        # 버튼 상태에 따른 출력
        if button_state == GPIO.LOW:
            print("Button Pressed")  # 버튼 눌림
        else:
            print("Button Released")  # 버튼이 눌리지 않음

        time.sleep(0.2)  # 0.2초 주기

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()  # 종료 시 GPIO 핀 정리
