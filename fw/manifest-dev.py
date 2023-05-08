include("$(PORT_DIR)/boards/manifest.py")
freeze('sub/micropython-mqtt/mqtt_as', ['mqtt_as.py'])
freeze('sub/micropython-font-to-py/writer', ['writer.py', 'freesans20.py'])

