import time
import mqtt_reg

import sys
sys.path.append('/')

import site_config

print('48V battery monitor')

registry = mqtt_reg.Registry(
    server=[
        # mqtt_reg.ServerRegister('A', {'gogo': 'logo'})
    ],
    wifi_ssid=site_config.wifi_ssid,
    wifi_password=site_config.wifi_password,
    mqtt_broker=site_config.mqtt_broker,
    ledPin=21,
    debug=site_config.debug
)

# registry.start()

