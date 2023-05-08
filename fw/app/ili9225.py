from machine import Pin, SPI
from micropython import const
import utime

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


def short_delay():
    utime.sleep_ms(50)

class ILI9225:

    def __init__(self, sck_pin=None, mosi_pin=None, rs_pin=None, rst_pin=None, ss_pin=None, bl_pin=None):

        self.spi = SPI(1, 40000000, sck=Pin(sck_pin), mosi=Pin(mosi_pin), miso=Pin(3))

        self.rst = Pin(rst_pin, Pin.OUT)
        self.rs = Pin(rs_pin, Pin.OUT)
        self.ss = Pin(ss_pin, Pin.OUT)

        self.ss.value(1)

        self.rst.value(1)
        short_delay()
        self.rst.value(0)
        short_delay()
        self.rst.value(1)
        short_delay()

        self.begin_tx()

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
        # self.set_register(ILI9225_GATE_SCAN_CTRL, 0x0000)
        # self.set_register(ILI9225_VERTICAL_SCROLL_CTRL1, 0x00DB)
        # self.set_register(ILI9225_VERTICAL_SCROLL_CTRL2, 0x0000)
        # self.set_register(ILI9225_VERTICAL_SCROLL_CTRL3, 0x0000)
        # self.set_register(ILI9225_PARTIAL_DRIVING_POS1, 0x00DB)
        # self.set_register(ILI9225_PARTIAL_DRIVING_POS2, 0x0000)
        # self.set_register(ILI9225_HORIZONTAL_WINDOW_ADDR1, 0x00AF)
        # self.set_register(ILI9225_HORIZONTAL_WINDOW_ADDR2, 0x0000)
        # self.set_register(ILI9225_VERTICAL_WINDOW_ADDR1, 0x00DB)
        # self.set_register(ILI9225_VERTICAL_WINDOW_ADDR2, 0x0000)
        # Set GAMMA curve
        # self.set_register(ILI9225_GAMMA_CTRL1, 0x0000)
        # self.set_register(ILI9225_GAMMA_CTRL2, 0x0808)
        # self.set_register(ILI9225_GAMMA_CTRL3, 0x080A)
        # self.set_register(ILI9225_GAMMA_CTRL4, 0x000A)
        # self.set_register(ILI9225_GAMMA_CTRL5, 0x0A08)
        # self.set_register(ILI9225_GAMMA_CTRL6, 0x0808)
        # self.set_register(ILI9225_GAMMA_CTRL7, 0x0000)
        # self.set_register(ILI9225_GAMMA_CTRL8, 0x0A00)
        # self.set_register(ILI9225_GAMMA_CTRL9, 0x0710)
        # self.set_register(ILI9225_GAMMA_CTRL10, 0x0710)
        # self.set_register(ILI9225_DISP_CTRL1, 0x0012)
        short_delay()
        self.set_register(ILI9225_DISP_CTRL1, 0x1017);


        self.rs.value(0)
        self.spi.write(bytes([ILI9225_GRAM_DATA_REG]))
        self.rs.value(1)
        for i in range(0, 100):
            for j in range(0, 120):
                self.spi.write(bytes([0xF0, 0xF0]))

        self.end_tx()

    def set_register(self, register, value):
        self.rs.value(0)
        self.spi.write(bytes([register]))
        self.rs.value(1)
        self.spi.write(bytes([value >> 8, value & 0xFF]))
        return self

    def begin_tx(self):
        self.ss.value(0)

    def end_tx(self):
        self.ss.value(1)

