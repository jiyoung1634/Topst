import RPi.GPIO as GPIO
import time

button_pin = 6  # 버튼을 연결할 GPIO 핀 번호 (실제 연결된 핀 번호로 수정 필요)

# GPIO 모드 설정 및 핀 초기화
GPIO.setmode(GPIO.BOARD)  # BOARD 모드 사용 (물리적 핀 번호 사용)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # 풀업 저항 활성화

try:
    while True:
        button_state = GPIO.input(button_pin)  # 버튼 상태 읽기
        if button_state == GPIO.LOW:
            print("Button Pressed")  # 버튼이 눌리면 "Button Pressed" 출력
        else:
            print("Button Released")  # 버튼이 눌리지 않으면 "Button Released" 출력
        time.sleep(0.1)  # 반복문 주기

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()  # 종료 시 GPIO 핀 정리
