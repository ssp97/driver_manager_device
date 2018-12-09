import public,requests,time

driver_time = 0
sw_num = 0
def display_file_w():
    global driver_time,sw_num
    now = time.time()
    rfid = public.temp_file.read("RFID")
    print(rfid)
    if rfid == None:
        public.temp_file.save("DISPLAY",["","请检查卡"])
    if rfid['time']+5 < now:
        public.temp_file.save("DISPLAY",["","请检查卡"])
    else:
        driver_time += 1
        #print(driver_time)
        if(driver_time > 10800):
            public.temp_file.save("DISPLAY",["","----注意----","","--疲劳驾驶!--"])
            return
        
        sw_num += 1
        if(sw_num==1):
            fatigue = public.temp_file.read("FATIGUE")
            if fatigue == -1:
                public.temp_file.save("DISPLAY",["--疲劳程度--"," ","没识别到人脸","请调整摄像头"])
                return
            #print(fatigue)
            public.temp_file.save("DISPLAY",["--疲劳程度--","",str(fatigue["fatigue"]),])
        elif(sw_num==2):
            alcohol = public.temp_file.read("ALCOHOL")
            public.temp_file.save("DISPLAY",["--酒精浓度--","",str(alcohol["alcohol"])])
        elif(sw_num==3):
            gps = public.temp_file.read("GPS")
            public.temp_file.save("DISPLAY",["----GPS----","",str(gps["longitude"]),str(gps["latitude"])])
        else:
            public.temp_file.save("DISPLAY",["--卡ID--","",rfid['uid']])
            sw_num=0
        #public.temp_file.save("DISPLAY",["","卡已经插入"])
def update():
    now = time.time()
    rfid = public.temp_file.read("RFID")
    gps = public.temp_file.read("GPS")
    fatigue = public.temp_file.read("FATIGUE")
    alcohol = public.temp_file.read("ALCOHOL")
    if rfid['time']+30 > now:
        data = {
            "driverId":rfid['uid'],
            "alcohol":alcohol["alcohol"],
            "fatigue":fatigue["fatigue"],
            "gpsX":gps["longitude"],
            "gpsY":gps["latitude"],
            "carId":2,
            }
        requests.get("http://139.199.68.189:81/driverstate_embedded_api",params = data)
        
def run():
    while True:
        for i in range(60):
            display_file_w()
            if i==30:update()
            print("beat")
            time.sleep(1)
        
if __name__ == "__main__":
    run()