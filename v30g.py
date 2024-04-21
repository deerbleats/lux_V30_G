from machine import Pin,SoftI2C
import time

"""
By DeerBleats
"""

POLYNOMIAL = 0x131
CONF_ADDR = 0x05
REBOOT_ADDR = 0xC0
RESET_ADDR = 0xB0
ADDR_CONF_ADDR = 0xA0
GENERNAL_ADDR = 0x00

class V30G(object):
    
    def __init__(self,i2c,enable_pin=None,addr=0x4a,with_shell = 1):
        self.i2c = i2c
        self.addr = addr
        self.enable_pin = enable_pin
        self.with_shell = with_shell
        self.is_started = 0


    def enable_moudle(self):
        if not self.enable_pin.value():
            if self.is_started ==0:
                self.enable_pin.value(1)
                print("please wait a seconds the moudle need time to initial")
                time.sleep(2)
                self.is_started = 1
            else:
                self.enable_pin.value(1)
        else:
            print("moudle already enable")
            pass

    def disable_moudle(self):
        if self.enable_pin.value():
            self.enable_pin.value(0)
            self.is_started = 0
        else:
            
            print("moudle already disable")
            self.is_started = 0
            pass
        
    def delay_10ms(self):
        time.sleep_ms(10)

    def delay_50ms(self):
        time.sleep_ms(50)



    def get_orginal_data(self):
        self.enable_moudle()
        orginal_list = bytearray(5)
        self.i2c.stop()
        self.delay_10ms()
        self.i2c.start()
        for i in range(5):
            orginal_data = self.i2c.readfrom_mem(self.addr,i,1)
            orginal_list[i] = orginal_data[0]
            print(orginal_data)
            self.delay_50ms()
        self.i2c.stop()
        print(orginal_list)
        if self.check_crc(orginal_list):
            print("crc ok")
            return orginal_list
        else:
            print("crc error")
            return(None)
            
    def writeto_target_addr(self,target_addr,mem_addr,data):
        self.enable_moudle()
        self.i2c.start()
        self.delay_10ms()
        self.i2c.writeto_mem(target_addr,mem_addr,data)
        self.delay_10ms()
        self.i2c.stop()


    def check_crc(self,data):
        # calculates 8-Bit checksum with given polynomial
        crc = 0xFF
        for b in data[:-1]:
            crc ^= b;
            for _ in range(8, 0, -1):
                if crc & 0x80:
                    crc = (crc << 1) ^ POLYNOMIAL
                else:
                    crc <<= 1
        crc_to_check = data[-1]
        return crc_to_check == crc

    def get_lux(self):
        data = self.get_orginal_data()
        if data is None:
            print("in get_lux func data is None please check crc or module is wrong")
            return None
        else:
            buf = data
            lf = buf[3]
            lf = (lf << 8)|buf[2]
            lf = (lf << 8)|buf[1]
            lf = (lf << 8)|buf[0]
            returnbuf = lf
            if self.with_shell:
                return float(returnbuf * 2.5) / 1000
            else:
                return float(returnbuf *1.4 ) / 1000

    def query_current_conf(self):

        self.enable_moudle()
        self.i2c.start()
        current_conf = self.i2c.readfrom_mem(self.addr,CONF_ADDR,1)
        self.i2c.stop()
        return current_conf[0]

    def change_conf(self,conf_level):
        self.enable_moudle()
        target_level = bytearray(1)
        target_level[0] = conf_level
        self.writeto_target_addr(self.addr,CONF_ADDR,target_level)
        print("change conf to %d"%conf_level)
        self.restart_device()

    def restart_device(self):
        self.writeto_target_addr(GENERNAL_ADDR,REBOOT_ADDR,b'\x00')
        print("moudle is rebooting")

    def reset_device(self):
        self.writeto_target_addr(GENERNAL_ADDR,RESET_ADDR,b'\x00')
        print("moudle is reset please wait a seconds")


    def change_device_addr(self,addr,immediately_reboot = 0):
        target_addr = bytearray(1)
        target_addr[0] = addr
        self.writeto_target_addr(GENERNAL_ADDR,ADDR_CONF_ADDR,target_addr)
        print("change v30g addr to %d"%addr)
        if immediately_reboot:
            self.restart_device()
        else:
            print("please reboot v30g to make changed addr effect")
            pass


if __name__ == "__main__":
    from v30g import V30G
    from machine import Pin,SoftI2C
    i2c = SoftI2C(scl=Pin(18), sda=Pin(19), freq=50000)
    enable_pin = Pin(2,Pin.OUT)
    lux_sensor = V30G(i2c=i2c,enable_pin=enable_pin)
    lux_sensor.get_lux()

    pass