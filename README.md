from v30g import V30G<br>
from machine import Pin,SoftI2C<br>
i2c = SoftI2C(scl=Pin(18), sda=Pin(19), freq=50000)<br>
enable_pin = Pin(2,Pin.OUT)<br>
lux_sensor = V30G(i2c=i2c,enable_pin=enable_pin)<br>
lux = lux_sensor.get_lux()<br>


