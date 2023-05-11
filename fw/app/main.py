import time
import mqtt_reg
import math
from machine import ADC, SPI, Pin

from ili9225 import ILI9225, Palette, ILI9225_HEIGHT, ILI9225_WIDTH

import sys
sys.path.append('/')
import site_config

spi = SPI(1, baudrate=10000000, polarity=0, phase=0, sck=Pin(site_config.dispSckPin), mosi=Pin(site_config.dispMosiPin), miso=Pin(site_config.dispMisoPin))
palette = Palette(2)
palette.set_color(0, 0, 0, 0)
palette.set_color(1, 100, 0, 50)
palette.set_color(2, 100, 50, 200)
palette.set_color(3, 255, 255, 255)
print("".join("\\x%02x" % i for i in palette.palette))
display = ILI9225(palette, spi, site_config.dispSsPin, site_config.dispRsPin, site_config.dispRstPin)

display.fill(0)
display.show()

for y in range(0, ILI9225_HEIGHT, 10):
    display.hline(0, y, ILI9225_WIDTH, 1)
for x in range(0, ILI9225_WIDTH, 10):
    display.vline(x, 0, ILI9225_HEIGHT, 2)

for y in range(0, ILI9225_HEIGHT, 10):
    display.text('y = ' + str(y), 0, y, 3)

c = 0
while True:
    display.rect(100, 100, 70, 10, 0, True)
    display.ellipse(80, c, 5, 5, 1+(c & 3), True)
    display.text(str(c), 100, 100, 3)
    display.show()
    c += 1
    if c > ILI9225_HEIGHT - 10:
        c = 0


# def ntc3950_resistance_to_temperature(resistance_ohm):
#     beta = 3950  # Beta value of NTC 3950 thermistor
#     r0 = 10000  # Resistance of NTC 3950 thermistor at 25 degrees Celsius
#     t0 = 25 + 273.15  # Temperature at which resistance of NTC 3950 thermistor is measured (in Kelvin)
#     t = 1 / ((1 / t0) + (1 / beta) * math.log(resistance_ohm / r0)) - 273.15  # Temperature in Celsius
#     return t

# print('48V battery monitor')

# voltage = mqtt_reg.ServerReadOnlyRegister(
#     site_config.name + '.voltage', {'device': site_config.name, 'unit': 'V', 'type': 'number'})
# current = mqtt_reg.ServerReadOnlyRegister(
#     site_config.name + '.current', {'device': site_config.name, 'unit': 'A', 'type': 'number'})
# temp = mqtt_reg.ServerReadOnlyRegister(
#     site_config.name + '.temp', {'device': site_config.name, 'unit': '°C', 'type': 'number'})

# registry = mqtt_reg.Registry(
#     server=[voltage, current, temp],
#     wifi_ssid=site_config.wifi_ssid,
#     wifi_password=site_config.wifi_password,
#     mqtt_broker=site_config.mqtt_broker,
#     ledPin=site_config.pinLed,
#     debug=site_config.debug
# )

# registry.start(background=True)

# print('Starting main loop')

# adcTemp = ADC(Pin(site_config.adcTemp), atten=ADC.ATTN_11DB)
# adcVoltage = ADC(Pin(site_config.adcVoltage), atten=ADC.ATTN_11DB)
# adcCurrent = ADC(Pin(site_config.adcCurrent), atten=ADC.ATTN_11DB)

# while True:
#     time.sleep(1)

#     def updateReg(reg, value):
#         if not value is None:
#             value = round(value, 1)
#             if not reg.value is None:
#                 value = round((value + reg.value) / 2, 1)
#         print(reg.name, value, reg.meta['unit'])
#         reg.set_value_local(value)

#     # read temperature

#     temp_adc_uV = adcTemp.read_uv() - site_config.adcOffset
#     if temp_adc_uV < 2800000:
#         temp_ohm = (temp_adc_uV * 27000) / (3300000 - temp_adc_uV)
#         temp_degC = ntc3950_resistance_to_temperature(temp_ohm)
#     else:
#         temp_degC = None
#     updateReg(temp, temp_degC)

#     # read voltage

#     voltage_adc_uV = adcVoltage.read_uv() - site_config.adcOffset
#     updateReg(voltage, voltage_adc_uV / (3.9/(100+3.9)) / 1000000)

#     # read current

#     current_adc_uV = adcCurrent.read_uv() - site_config.adcOffset
#     current_div_uV = current_adc_uV * (27000 + 100000) / 100000
#     current_Amps = site_config.currentProbeAmps * (current_div_uV - 2500000) / 625000
#     updateReg(current, current_Amps)
