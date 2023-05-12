import ili9225
import freesans20

from machine import SPI, Pin

class Display:
    def __init__(self, site_config):
        spi = SPI(1, baudrate=40000000, polarity=0, phase=0, sck=Pin(site_config.dispSckPin), mosi=Pin(site_config.dispMosiPin), miso=Pin(site_config.dispMisoPin))

        self.ili = ili9225.ILI9225(spi, site_config.dispSsPin, site_config.dispRsPin, site_config.dispRstPin, rotation=1)
        self.ili.clear()

        self.x1 = self.ili.width // 3
        self.x2 = 2 * self.ili.width // 3

    def update(self, voltage, current, temp):

        self.ili.print(str(voltage) +'V', self.x1, 10, freesans20, fg_color=0xFFFFFF, bg_color=0x101010, align=ili9225.ALIGN_RIGHT, x2=self.x2)
        self.ili.print(str(current) +'A', self.x1, 60, freesans20, fg_color=0xFFFFFF, bg_color=0x101010, align=ili9225.ALIGN_RIGHT, x2=self.x2)
        self.ili.print(str(temp) +'oC', self.x1, 110, freesans20, fg_color=0xFFFFFF, bg_color=0x101010, align=ili9225.ALIGN_RIGHT, x2=self.x2)
