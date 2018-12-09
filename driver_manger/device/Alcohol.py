# coding=utf-8
import smbus2 as smbus
import public,time

class PCF8591:
    def __init__(self, bus=1, address=0x48):
        #print('[*]PCF8591 Init Start!')
        self.bus = smbus.SMBus(bus)
        self.address = address
        #print('[+]GY30 Init OK!')

    def help(self):
        print('now address:0x%x' % self.address)
        print('接上P4 短路帽，选择热敏电阻接入电路')
        print('接上P5 短路帽，选择光敏电阻接入电路')
        print('接上P6 短路帽，选择0-5V可调电压接入电路')
        print('AIN0：光敏电阻AD转换值')
        print('AIN1：热敏电阻AD转换值 ')
        print('AIN2：悬空')
        print('AIN3：0-5V可调电压转换值（蓝色电位器调节）')

    def read_AIN0(self):
        self.bus.write_byte(self.address, 0x40)
        self.bus.read_byte(self.address)  # dummy read to start conversion
        return self.bus.read_byte(self.address)

    def read_AIN1(self):
        self.bus.write_byte(self.address, 0x41)
        self.bus.read_byte(self.address)  # dummy read to start conversion
        return self.bus.read_byte(self.address)

    def read_AIN2(self):
        self.bus.write_byte(self.address, 0x42)
        self.bus.read_byte(self.address)  # dummy read to start conversion
        return self.bus.read_byte(self.address)

    def read_AIN3(self):
        self.bus.write_byte(self.address, 0x43)
        self.bus.read_byte(self.address)  # dummy read to start conversion
        return self.bus.read_byte(self.address)

def run():
    while True:
        try:
            test = PCF8591()
            result = 0
            for _ in range(10):
                result += test.read_AIN0()/10
            public.temp_file.save("ALCOHOL",{"alcohol":int(result)})
            time.sleep(30)
            del test
        except:
            print("err")
            del test

if __name__ == '__main__':
    run()
