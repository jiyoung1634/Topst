from ..Library.Module import LCD_Display_Library as lcd
import time

lcd_pins = [117, 121, 114, 113, 112, 61]

if __name__ == "__main__":
    try:
        lcd.set_device(lcd_pins)
        while True:
            lcd.byte_transfer("Hello, World!", 0)
            lcd.byte_transfer("Line 2 here", 1)
            time.sleep(3)
            lcd.byte_transfer("LCD Test", 0)
            lcd.byte_transfer("Goodbye!", 1)
            time.sleep(3)
    except KeyboardInterrupt:
        print("\nProgram stopped by User")
    finally:
        lcd.quit_device(lcd_pins)