import time
import mqtt_reg

import sys
sys.path.append('/')
import site_config


print('48V battery monitor')

voltage = mqtt_reg.ServerReadOnlyRegister(site_config.name + '.voltage', {'device': site_config.name, 'unit': 'V', 'type': 'number'})
current = mqtt_reg.ServerReadOnlyRegister(site_config.name + '.current', {'device': site_config.name, 'unit': 'A', 'type': 'number'})
power = mqtt_reg.ServerReadOnlyRegister(site_config.name + '.power', {'device': site_config.name, 'unit': 'W', 'type': 'number'})
temp = mqtt_reg.ServerReadOnlyRegister(site_config.name + '.temp', {'device': site_config.name, 'unit': '°C', 'type': 'number'})

registry = mqtt_reg.Registry(
    server=[voltage, current, power],
    wifi_ssid=site_config.wifi_ssid,
    wifi_password=site_config.wifi_password,
    mqtt_broker=site_config.mqtt_broker,
    ledPin=21,
    debug=site_config.debug
)

registry.start()
