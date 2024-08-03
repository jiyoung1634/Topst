import os
import time
import smbus

# I2C 버스 설정
bus = smbus.SMBus(1)
address = 0x48

# GPIO 핀 번호 설정
LED1_PIN = 84  # 물이 없는 상태에서 켜지는 LED
LED2_PIN = 85  # 물이 중간 정도일 때 켜지는 LED
LED3_PIN = 86  # 물이 꽉 찼을 때 켜지는 LED

# GPIO 경로 설정
GPIO_BASE_PATH = "/sys/class/gpio"
GPIO_EXPORT_PATH = os.path.join(GPIO_BASE_PATH, "export")
GPIO_UNEXPORT_PATH = os.path.join(GPIO_BASE_PATH, "unexport")

# GPIO 핀 제어 함수
def gpio_export(pin):
    """GPIO 핀을 활성화합니다."""
    if not os.path.exists(os.path.join(GPIO_BASE_PATH, f"gpio{pin}")):
        with open(GPIO_EXPORT_PATH, "w") as f:
            f.write(str(pin))

def gpio_unexport(pin):
    """GPIO 핀을 비활성화합니다."""
    if os.path.exists(os.path.join(GPIO_BASE_PATH, f"gpio{pin}")):
        with open(GPIO_UNEXPORT_PATH, "w") as f:
            f.write(str(pin))

def gpio_direction(pin, direction):
    """GPIO 핀의 방향을 설정합니다."""
    direction_path = os.path.join(GPIO_BASE_PATH, f"gpio{pin}", "direction")
    with open(direction_path, "w") as f:
        f.write(direction)

def gpio_write(pin, value):
    """GPIO 핀의 값을 설정합니다."""
    value_path = os.path.join(GPIO_BASE_PATH, f"gpio{pin}", "value")
    with open(value_path, "w") as f:
        f.write(str(value))

def read_pcf8591(channel, retries=5):
    """PCF8591에서 아날로그 값을 읽어옵니다."""
    if channel < 0 or channel > 3:
        raise ValueError("Invalid channel: {}".format(channel))
    
    for attempt in range(retries):
        try:
            bus.write_byte(address, 0x40 | channel)
            value = bus.read_byte(address)
            return value
        except IOError as e:
            print(f"Attempt {attempt + 1} failed with error: {e}")
            time.sleep(0.1)
    raise IOError("Failed to communicate with PCF8591 after multiple attempts")

def control_leds(value):
    if 20 < value < 65:  # LOW
        gpio_write(LED1_PIN, 1)
        gpio_write(LED2_PIN, 0)
        gpio_write(LED3_PIN, 0)
    elif 65 < value < 170:  # HIGH
        gpio_write(LED1_PIN, 0)
        gpio_write(LED2_PIN, 1)
        gpio_write(LED3_PIN, 0)
    else:  # 0 (not detected water)
        gpio_write(LED1_PIN, 0)
        gpio_write(LED2_PIN, 0)
        gpio_write(LED3_PIN, 1)

# GPIO 초기화
gpio_export(LED1_PIN)
gpio_export(LED2_PIN)
gpio_export(LED3_PIN)

gpio_direction(LED1_PIN, "out")
gpio_direction(LED2_PIN, "out")
gpio_direction(LED3_PIN, "out")

try:
    while True:
        try:
            value = read_pcf8591(0)  # 센서 값 읽기
            print("Sensor value: {}".format(value))
            control_leds(value)
        except IOError as e:
            print("I2C communication error: ", e)
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    gpio_unexport(LED1_PIN)
    gpio_unexport(LED2_PIN)
    gpio_unexport(LED3_PIN)
    bus.close()
