import time
import mqtt_reg
import math
from machine import ADC, ADCBlock, Pin

from ili9225 import ILI9225

import sys
sys.path.append('/')
import site_config

def ntc3950_resistance_to_temperature(resistance_ohm):
    beta = 3950  # Beta value of NTC 3950 thermistor
    r0 = 10000  # Resistance of NTC 3950 thermistor at 25 degrees Celsius
    t0 = 25 + 273.15  # Temperature at which resistance of NTC 3950 thermistor is measured (in Kelvin)
    t = 1 / ((1 / t0) + (1 / beta) * math.log(resistance_ohm / r0)) - 273.15  # Temperature in Celsius
    return t

print('48V battery monitor')

voltage = mqtt_reg.ServerReadOnlyRegister(
    site_config.name + '.voltage', {'device': site_config.name, 'unit': 'V', 'type': 'number'})
current = mqtt_reg.ServerReadOnlyRegister(
    site_config.name + '.current', {'device': site_config.name, 'unit': 'A', 'type': 'number'})
temp = mqtt_reg.ServerReadOnlyRegister(
    site_config.name + '.temp', {'device': site_config.name, 'unit': '°C', 'type': 'number'})

registry = mqtt_reg.Registry(
    server=[voltage, current, temp],
    wifi_ssid=site_config.wifi_ssid,
    wifi_password=site_config.wifi_password,
    mqtt_broker=site_config.mqtt_broker,
    ledPin=site_config.pinLed,
    debug=site_config.debug
)

registry.start(background=True)

print('Starting main loop')

adcTemp = ADC(Pin(site_config.adcTemp), atten=ADC.ATTN_11DB)
adcVoltage = ADC(Pin(site_config.adcVoltage), atten=ADC.ATTN_11DB)
adcCurrent = ADC(Pin(site_config.adcCurrent), atten=ADC.ATTN_11DB)

display = ILI9225(sck_pin=site_config.dispSckPin, mosi_pin=site_config.dispMosiPin, rs_pin=site_config.dispRsPin, rst_pin=site_config.dispRstPin, ss_pin=site_config.dispSsPin, bl_pin=site_config.dispBlPin)

while True:
    time.sleep(1)

    def updateReg(reg, value):
        if not value is None:
            value = round(value, 1)
            if not reg.value is None:
                value = round((value + reg.value) / 2, 1)
        print(reg.name, value, reg.meta['unit'])
        reg.set_value_local(value)

    # read temperature

    temp_adc_uV = adcTemp.read_uv() - site_config.adcOffset
    if temp_adc_uV < 2800000:
        temp_ohm = (temp_adc_uV * 27000) / (3300000 - temp_adc_uV)
        temp_degC = ntc3950_resistance_to_temperature(temp_ohm)
    else:
        temp_degC = None
    updateReg(temp, temp_degC)

    # read voltage

    voltage_adc_uV = adcVoltage.read_uv() - site_config.adcOffset
    updateReg(voltage, voltage_adc_uV / (3.9/(100+3.9)) / 1000000)

    # read current

    current_adc_uV = adcCurrent.read_uv() - site_config.adcOffset
    current_div_uV = current_adc_uV * (27000 + 100000) / 100000
    current_Amps = site_config.currentProbeAmps * (current_div_uV - 2500000) / 625000
    updateReg(current, current_Amps)