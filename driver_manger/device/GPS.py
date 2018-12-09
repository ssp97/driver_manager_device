#! /usr/bin/python3

import serial,public,time
ATGM332D_DEBUG = False

class ATGM332D:
    def __init__(self):
        #print('[*]ATGM332D Init Start!')
        COM_NUM = 0
        while COM_NUM<100:
            try:
                self.ser = serial.Serial('/dev/ttyUSB'+str(COM_NUM), 9600)
                if ATGM332D_DEBUG:print('[+]ATGM332D Init OK! ttyUSB'+str(COM_NUM))
                break
            except:
                COM_NUM = COM_NUM + 1

    def readData(self):
        text = self.readText()
        if text[6] == '1':
            result = {
                'longitude':(round(float(text[4]) / 100, 6), text[5]),  # 经度
                'latitude': (round(float(text[2]) / 100, 6), text[3]),  # 纬度
                'height':text[9],
            }
        else:
            if ATGM332D_DEBUG:print(text)
            result = {
                'longitude': -1,
                'latitude': -1,
                'height': -1,
            }
        return result

    def readText(self):
        while True:
            recv = self.ser.readline().decode().replace('\r\n', '').split(',')
            if recv[0] == '$GNGGA':  # 开始获取信息
                return recv

def run():
    test = None
    while True:
        try:
            test = ATGM332D()
            public.temp_file.save("GPS",test.readData())
            del test
            time.sleep(20)
        except:
            print("[ERR]GPS NOT FOUND!")

if __name__ == '__main__':
    ATGM332D_DEBUG = True
    run()