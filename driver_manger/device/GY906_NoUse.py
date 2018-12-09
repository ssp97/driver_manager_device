import smbus
import time


class GY30:
    def __init__(self, busnum=1, addr=0x5a):
        print('[*]GY906 Init Start!')
        self.__bus = smbus.SMBus(busnum)
        self.__addr = addr
        print('[+]GY906 Init OK!')

    def readData(self):
        temp = self.__bus.read_word_data(self.__addr,0x07)
        temp = (temp * 0.02) - 273.15
        return round(temp, 2)



if __name__ == '__main__':
    dev = GY30()
    while True:
        print(dev.readData())
        time.sleep(1)
