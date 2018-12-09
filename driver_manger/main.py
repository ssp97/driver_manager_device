#! /usr/bin/python3

from multiprocessing import Pool
import time
import Alcohol,Camera,GPS,Oled,Rfid,public

def run_device():
    pool =Pool(5)
    pool.apply(func=f1,args=(Alcohol.run,))
    pool.apply(func=f1,args=(Camera.run,))
    pool.apply(func=f1,args=(GPS.run,))
    pool.apply(func=f1,args=(Oled.run,))
    pool.apply(func=f1,args=(Rfid.run,))
    pool.close()
    pool.join()


if __name__=="__main__":
    run_device()




