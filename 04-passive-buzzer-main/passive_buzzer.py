import sys
import os
import time
import threading
import IPC_Library

GPIO_EXPORT_PATH = "/sys/class/gpio/export"
GPIO_UNEXPORT_PATH = "/sys/class/gpio/unexport"
GPIO_DIRECTION_PATH_TEMPLATE = "/sys/class/gpio/gpio{}/direction"
GPIO_VALUE_PATH_TEMPLATE = "/sys/class/gpio/gpio{}/value"
GPIO_BASE_PATH_TEMPLATE = "/sys/class/gpio/gpio{}"

FREQUENCIES = {
    'C': 261.63,  
    'D': 293.66,  
    'E': 329.63,  
    'F': 349.23,  
    'G': 392.00,  
    'A': 440.00,  
    'B': 493.88,  
    'C5': 523.25  
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
            print(f"Error exporting GPIO: {e}")
            sys.exit(1)

def unexport_gpio(gpio_number):
    try:
        with open(GPIO_UNEXPORT_PATH, 'w') as unexport_file:
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

def ipc_listener():
    """CAN 통신을 통해 수신한 메시지를 처리하는 함수"""
    while True:
        try:
            print("IPC_Library.received_pucData", ' '.join(format(byte, '02X') for byte in IPC_Library.received_pucData))
            
            if IPC_Library.received_pucData:
                if IPC_Library.received_pucData[0] == 1:
                    print("Playing C")
                    play_tone(gpio_pin, FREQUENCIES['C'], 0.5)
                elif IPC_Library.received_pucData[0] == 2:
                    print("Playing D")
                    play_tone(gpio_pin, FREQUENCIES['D'], 0.5)
                # 추가적으로 다른 데이터 처리
                else:
                    print("No relevant data received.")
            time.sleep(0.1)
        except Exception as e:
            print(f"Error in IPC listener: {e}")
            time.sleep(1)  # 예외 발생 시 잠시 대기 후 계속 진행

def play_tone(gpio_number, frequency, duration):
    period = 1.0 / frequency
    half_period = period / 2
    end_time = time.time() + duration

    while time.time() < end_time:
        set_gpio_value(gpio_number, 1)
        time.sleep(half_period)
        set_gpio_value(gpio_number, 0)
        time.sleep(half_period)

if __name__ == "__main__":
    gpio_pin = 89  # 사용할 GPIO 핀 번호

    try:
        # IPC 통신을 위한 쓰레드 실행
        ipc_thread = threading.Thread(target=ipc_listener)
        ipc_thread.daemon = True  # 데몬 쓰레드로 설정하여 프로그램 종료 시 자동으로 종료되게
        ipc_thread.start()

        # GPIO 초기화
        export_gpio(gpio_pin)
        set_gpio_direction(gpio_pin, "out")

        # 메인 루프 - CAN 메시지를 계속 기다리며 처리
        while True:
            pass  # 지속적으로 IPC 데이터를 처리합니다.

    except KeyboardInterrupt:
        print("\nProgram interrupted")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        unexport_gpio(gpio_pin)

    sys.exit(0)
