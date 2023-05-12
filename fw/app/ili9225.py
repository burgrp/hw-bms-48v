from machine import Pin, SPI
from micropython import const
import utime
import framebuf

# https://www.displayfuture.com/Display/datasheet/controller/ILI9225.pdf

# Register definitions

# Control registers
ILI9225_DRIVER_OUTPUT_CTRL=const(0x01)  # Driver Output Control
ILI9225_LCD_AC_DRIVING_CTRL=const(0x02)  # LCD AC Driving Control
ILI9225_ENTRY_MODE=const(0x03)  # Entry Mode
ILI9225_DISP_CTRL1=const(0x07)  # Display Control 1
ILI9225_DISP_CTRL2=const(0x08)  # Blank Period Control
ILI9225_FRAME_CYCLE_CTRL=const(0x0B)  # Frame Cycle Control
ILI9225_INTERFACE_CTRL=const(0x0C)  # Interface Control
ILI9225_OSC_CTRL=const(0x0F)  # Osc Control
ILI9225_POWER_CTRL1=const(0x10)  # Power Control 1
ILI9225_POWER_CTRL2=const(0x11)  # Power Control 2
ILI9225_POWER_CTRL3=const(0x12)  # Power Control 3
ILI9225_POWER_CTRL4=const(0x13)  # Power Control 4
ILI9225_POWER_CTRL5=const(0x14)  # Power Control 5
ILI9225_VCI_RECYCLING=const(0x15)  # VCI Recycling
ILI9225_RAM_ADDR_SET1=const(0x20)  # Horizontal GRAM Address Set
ILI9225_RAM_ADDR_SET2=const(0x21)  # Vertical GRAM Address Set
ILI9225_GRAM_DATA_REG=const(0x22)  # GRAM Data Register
ILI9225_GATE_SCAN_CTRL=const(0x30)  # Gate Scan Control Register
ILI9225_VERTICAL_SCROLL_CTRL1=const(0x31)  # Vertical Scroll Control 1 Register
ILI9225_VERTICAL_SCROLL_CTRL2=const(0x32)  # Vertical Scroll Control 2 Register
ILI9225_VERTICAL_SCROLL_CTRL3=const(0x33)  # Vertical Scroll Control 3 Register
ILI9225_PARTIAL_DRIVING_POS1=const(0x34)  # Partial Driving Position 1 Register
ILI9225_PARTIAL_DRIVING_POS2=const(0x35)  # Partial Driving Position 2 Register
ILI9225_HORIZONTAL_WINDOW_ADDR1=const(0x36)  # Horizontal Address Start Position (Window-HStart)
ILI9225_HORIZONTAL_WINDOW_ADDR2=const(0x37)  # Horizontal Address End Position   (Window-HEnd)
ILI9225_VERTICAL_WINDOW_ADDR1=const(0x38)  # Vertical Address Start Position	  (Window-VStart)
ILI9225_VERTICAL_WINDOW_ADDR2=const(0x39)  # Vertical Address End Position	  (Window-VEnd)
ILI9225_GAMMA_CTRL1=const(0x50)  # Gamma Control 1
ILI9225_GAMMA_CTRL2=const(0x51)  # Gamma Control 2
ILI9225_GAMMA_CTRL3=const(0x52)  # Gamma Control 3
ILI9225_GAMMA_CTRL4=const(0x53)  # Gamma Control 4
ILI9225_GAMMA_CTRL5=const(0x54)  # Gamma Control 5
ILI9225_GAMMA_CTRL6=const(0x55)  # Gamma Control 6
ILI9225_GAMMA_CTRL7=const(0x56)  # Gamma Control 7
ILI9225_GAMMA_CTRL8=const(0x57)  # Gamma Control 8
ILI9225_GAMMA_CTRL9=const(0x58)  # Gamma Control 9
ILI9225_GAMMA_CTRL10=const(0x59)  # Gamma Control 10

ILI9225_WIDTH=const(176)
ILI9225_HEIGHT=const(220)

def short_delay():
    utime.sleep_ms(50)

class Palette:
    def __init__(self, channel_bits):
        self.channel_bits = channel_bits
        self.palette = bytearray(2 << channel_bits)

    def set_color(self, index, r, g, b):
        # convert 8-bit RGB to 16-bit RGB565
        self.palette[index * 2] = (r & 0xF8) | (g >> 5)
        self.palette[index * 2 + 1] = ((g & 0x1C) << 3) | (b >> 3)

class ILI9225():

    def __init__(self, palette, spi, ss_pin, rs_pin, rst_pin):

        self.width = ILI9225_WIDTH
        self.height = ILI9225_HEIGHT

        self.palette = palette

        self.spi = spi

        self.ss = Pin(ss_pin, Pin.OUT)
        self.rs = Pin(rs_pin, Pin.OUT)
        self.rst = Pin(rst_pin, Pin.OUT)

        self.ss.value(1)

        self.rst.value(1)
        short_delay()
        self.rst.value(0)
        short_delay()
        self.rst.value(1)
        short_delay()

        self.tx_begin()

	    # Power-on sequence
        self.set_register(ILI9225_POWER_CTRL1, 0x0000)
        self.set_register(ILI9225_POWER_CTRL2, 0x0000)
        self.set_register(ILI9225_POWER_CTRL3, 0x0000)
        self.set_register(ILI9225_POWER_CTRL4, 0x0000)
        self.set_register(ILI9225_POWER_CTRL5, 0x0000)
        short_delay()
        # Power-on sequence
        self.set_register(ILI9225_POWER_CTRL2, 0x0018)
        self.set_register(ILI9225_POWER_CTRL3, 0x6121)
        self.set_register(ILI9225_POWER_CTRL4, 0x006F)
        self.set_register(ILI9225_POWER_CTRL5, 0x495F)
        self.set_register(ILI9225_POWER_CTRL1, 0x0F00)
        short_delay()
        self.set_register(ILI9225_POWER_CTRL2, 0x103B)
        short_delay()
        self.set_register(ILI9225_DRIVER_OUTPUT_CTRL, 0x011C)
        self.set_register(ILI9225_LCD_AC_DRIVING_CTRL, 0x0100)
        self.set_register(ILI9225_ENTRY_MODE, 0x01030)
        self.set_register(ILI9225_DISP_CTRL1, 0x0000)
        self.set_register(ILI9225_DISP_CTRL2, 0x0808)
        self.set_register(ILI9225_FRAME_CYCLE_CTRL, 0x1100)
        self.set_register(ILI9225_INTERFACE_CTRL, 0x0000)
        self.set_register(ILI9225_OSC_CTRL, 0x0D01)
        self.set_register(ILI9225_VCI_RECYCLING, 0x0020)
        self.set_register(ILI9225_RAM_ADDR_SET1, 0x0000)
        self.set_register(ILI9225_RAM_ADDR_SET2, 0x0000)
        # Set GRAM area
        self.set_register(ILI9225_GATE_SCAN_CTRL, 0x0000)
        self.set_register(ILI9225_VERTICAL_SCROLL_CTRL1, 0x00DB)
        self.set_register(ILI9225_VERTICAL_SCROLL_CTRL2, 0x0000)
        self.set_register(ILI9225_VERTICAL_SCROLL_CTRL3, 0x0000)
        self.set_register(ILI9225_PARTIAL_DRIVING_POS1, 0x00DB)
        self.set_register(ILI9225_PARTIAL_DRIVING_POS2, 0x0000)
        self.set_register(ILI9225_HORIZONTAL_WINDOW_ADDR1, 0x00AF)
        self.set_register(ILI9225_HORIZONTAL_WINDOW_ADDR2, 0x0000)
        self.set_register(ILI9225_VERTICAL_WINDOW_ADDR1, 0x00DB)
        self.set_register(ILI9225_VERTICAL_WINDOW_ADDR2, 0x0000)
        # Set GAMMA curve
        self.set_register(ILI9225_GAMMA_CTRL1, 0x0000)
        self.set_register(ILI9225_GAMMA_CTRL2, 0x0808)
        self.set_register(ILI9225_GAMMA_CTRL3, 0x080A)
        self.set_register(ILI9225_GAMMA_CTRL4, 0x000A)
        self.set_register(ILI9225_GAMMA_CTRL5, 0x0A08)
        self.set_register(ILI9225_GAMMA_CTRL6, 0x0808)
        self.set_register(ILI9225_GAMMA_CTRL7, 0x0000)
        self.set_register(ILI9225_GAMMA_CTRL8, 0x0A00)
        self.set_register(ILI9225_GAMMA_CTRL9, 0x0710)
        self.set_register(ILI9225_GAMMA_CTRL10, 0x0710)
        self.set_register(ILI9225_DISP_CTRL1, 0x0012)
        short_delay()
        self.set_register(ILI9225_DISP_CTRL1, 0x1017);

        self.tx_end()


    def set_register(self, register, value):
        self.rs.value(0)
        self.spi.write(bytes([register]))
        self.rs.value(1)
        self.spi.write(bytes([value >> 8, value & 0xFF]))
        return self

    def tx_begin(self):
        self.ss.value(0)

    def tx_end(self):
        self.ss.value(1)

    def window_begin(self, x, y, width, height):
        self.tx_begin()

        self.set_register(ILI9225_RAM_ADDR_SET1, x)
        self.set_register(ILI9225_RAM_ADDR_SET2, y)
        self.set_register(ILI9225_HORIZONTAL_WINDOW_ADDR1, x + width -1)
        self.set_register(ILI9225_HORIZONTAL_WINDOW_ADDR2, x)
        self.set_register(ILI9225_VERTICAL_WINDOW_ADDR1, y + height - 1)
        self.set_register(ILI9225_VERTICAL_WINDOW_ADDR2, y)

        self.rs.value(0)
        self.spi.write(bytes([ILI9225_GRAM_DATA_REG]))
        self.rs.value(1)

    def window_end(self):
        self.tx_end()


    def bitmap(self, bitmap, x, y, width, height, color):

        self.window_begin(x, y, width, height)

        palette = self.palette.palette

        expanded = bytearray(2 * width * height)

        bit_offset = 0
        for y in range(height):
            for x in range(width):
                pixel = (bitmap[bit_offset // 8] >> (7-(bit_offset % 8))) & 1
                palette_index = 2*color*pixel
                expanded_index = 2 * (y * width + x)
                expanded[expanded_index] = palette[palette_index]
                expanded[expanded_index + 1] = palette[palette_index + 1]
                bit_offset += 1
            if bit_offset % 8 != 0:
                bit_offset += 8 - (bit_offset % 8)

        self.spi.write(expanded)

        self.window_end()

    def print(self, text, x, y, font, color = 1):
        (bitmap, height, width) = font.get_ch(text)
        self.bitmap(bitmap, x, y, width, height, color)

    def fill_rect(self, x, y, width, height, color = 1):
        self.window_begin(x, y, width, height)

        palette_index = 2 * color
        byte0 = self.palette.palette[palette_index]
        byte1 = self.palette.palette[palette_index + 1]

        count = 2 * width * height
        buffer_len = min(count, 4096)
        buffer = bytearray(buffer_len)

        for i in range(buffer_len // 2):
            buffer[2*i] = byte0
            buffer[2*i + 1] = byte1

        while count > 0:
            if count < buffer_len:
                buffer = memoryview(buffer)[:count]
            self.spi.write(buffer)
            count -= buffer_len
            self.spi.write(buffer)

        self.window_end()

    def hline(self, x, y, width, color = 1):
        self.fill_rect(x, y, width, 1, color)

    def vline(self, x, y, height, color = 1):
        self.fill_rect(x, y, 1, height, color)

    def clear(self, color = 0):
        self.fill_rect(0, 0, self.width, self.height, color)

