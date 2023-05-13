import ili9225
#import freesans20 as font
import font

from machine import SPI, Pin

def reg_to_str(reg):
    if reg.value is None:
        return '(none)'
    else:
        return str(reg.value) + ' ' + reg.meta['unit']

class Display:
    def __init__(self, site_config):
        spi = SPI(1, baudrate=40000000, polarity=0, phase=0, sck=Pin(site_config.dispSckPin), mosi=Pin(site_config.dispMosiPin), miso=Pin(site_config.dispMisoPin))

        self.ili = ili9225.ILI9225(spi, site_config.dispSsPin, site_config.dispRsPin, site_config.dispRstPin, rotation=1)
        self.ili.clear()

        self.x1 = self.ili.width // 5
        self.x2 = 4 * self.ili.width // 5

        self.div1 = self.ili.height // 3
        self.div2 = 2 * self.ili.height // 3

    def update(self, voltage, current, temp, online):

        bg_color = 0x000000
        current_color = 0x00FF99 if current.value and current.value < 0 else 0x00CCFF
        pad_top = 12
        self.ili.print(reg_to_str(voltage), self.x1, pad_top, font, fg_color=0xFFFFFF, bg_color=bg_color, align=ili9225.ALIGN_RIGHT, x2=self.x2)
        self.ili.print(reg_to_str(current), self.x1, self.div1 + pad_top, font, fg_color=current_color, bg_color=bg_color, align=ili9225.ALIGN_RIGHT, x2=self.x2)
        self.ili.print(reg_to_str(temp), self.x1, self.div2 + pad_top, font, fg_color=0xFFFFFF, bg_color=bg_color, align=ili9225.ALIGN_RIGHT, x2=self.x2)

        line_color = 0x00FF99 if online else 0xFF0000
        self.ili.hline(0, self.div1, self.ili.width, line_color)
        self.ili.hline(0, self.div2, self.ili.width, line_color)
