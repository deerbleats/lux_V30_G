'''
from v30g import V30G
from machine import Pin,SoftI2C
i2c = SoftI2C(scl=Pin(18), sda=Pin(19), freq=50000)
enable_pin = Pin(2,Pin.OUT)
lux_sensor = V30G(i2c=i2c,enable_pin=enable_pin)
lux_sensor.get_lux()
'''
