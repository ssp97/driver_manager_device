#! /usr/bin/python3

from multiprocessing import Pool
import time
import Alcohol,Camera,GPS,Oled,Rfid,public,web

def run_device():
    pool =Pool(6)
    pool.apply_async(func=Alcohol.run)
    pool.apply_async(func=Camera.run)
    pool.apply_async(func=GPS.run)
    pool.apply_async(func=Oled.run)
    pool.apply_async(func=Rfid.run)
    pool.apply_async(func=web.run)
    pool.close()
    print("system start")
    try:
        pool.join()
    except:
        pool.terminate()
    


if __name__=="__main__":
    run_device()




