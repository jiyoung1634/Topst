import RPi.GPIO as GPIO
import time

button_pin = 6  # 버튼을 연결할 GPIO 핀 번호

GPIO.setmode(GPIO.BOARD)  # BOARD 모드 사용
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # 버튼 핀을 입력으로 설정, 풀업 저항 활성화

try:
    while True:
        button_state = GPIO.input(button_pin)  # 버튼 상태 읽기
        print(f"GPIO {button_pin} state: {button_state}")  # GPIO 상태 출력

        if button_state == GPIO.LOW:
            print("Button Pressed")  # 버튼 눌림 상태
        else:
            print("Button Released")  # 버튼이 눌리지 않았을 때
        time.sleep(0.2)  # 0.2초 주기

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()  # 종료 시 GPIO 핀 정리
