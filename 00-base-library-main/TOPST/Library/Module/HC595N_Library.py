from .. import Soft_SPI_Library as spi

# set spi for use device
def set_spi(mosi_pin, sclk_pin, rclk_pin):
    spi.set_soft_spi(0, mosi_pin, 0, sclk_pin, rclk_pin)

# transfer data to 74HC595N register
def transfer_data(data, mosi_pin, sclk_pin):
    spi.write_data(data,  mosi_pin, sclk_pin)

# unexport spi after using device
def clear_spi(mosi_pin, sclk_pin, rclk_pin):
    spi.clear_soft_spi(0, mosi_pin,0,sclk_pin, rclk_pin)