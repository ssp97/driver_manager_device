# coding=utf-8
import numpy as np
import requests
import cv2
import io
import json
from requests_toolbelt import MultipartEncoder
from PIL import Image
import public,time


class Camera:
    def __init__(self):
        self.face_url = 'https://api-cn.faceplusplus.com/facepp/v3/detect'
        self.camera = cv2.VideoCapture(0)
        for _ in range(10):
            _, img = self.camera.read()

    def face(self,img):
        # multipart/form-data post
        params = MultipartEncoder(fields={
            'api_key': '4ixDXgaKthUlINcvWXf7d_inECVosMIg',
            'api_secret': 'en0EvGSXpAvaUT5fIqNlxykvbfUsTaeK',
            'image_file': (" ",img,'application/octet-stream'),
            'return_landmark': '1',
            'return_attributes': 'eyestatus'
        })

        res = requests.post(
            url=self.face_url,
            data=params,
            headers={'Content-Type': params.content_type}
        )
        content = json.loads(res.text)
        result = 0
        if len(content['faces'])!=0:
            eyestate = content['faces'][0]['attributes']['eyestatus']
            print(eyestate)
            left_eye_status = eyestate['left_eye_status']
            right_eye_status = eyestate['right_eye_status']
            left_eye_status.pop('dark_glasses')
            right_eye_status.pop('dark_glasses')
            
            result += left_eye_status['normal_glass_eye_close']+left_eye_status['no_glass_eye_close']
            result += right_eye_status['normal_glass_eye_close']+right_eye_status['no_glass_eye_close']
            
            #result +=(left_eye_status['occlusion']+left_eye_status['dark_glasses'])/2
            #result +=(right_eye_status['occlusion']+right_eye_status['dark_glasses'])/2
            
            #print(max(left_eye_status,key=left_eye_status.get))
            #print(max(right_eye_status,key=right_eye_status.get))
        else:
            result = -1
        return result

    def readData(self,num):
        _, img = self.camera.read()
        # 图片转换为二进制数据
        _, buf = cv2.imencode(".jpg", img)
        img = Image.fromarray(np.uint8(buf)).tobytes()
        img = io.BytesIO(img)
        return self.face(img)

    def __del__(self):
        self.camera.release()

def run():
    while True:
        try:
            test = Camera()
            num,fatigue = 0,0
            for _ in range(10):
                result = test.readData(_)
                if result != -1:
                    num += 1
                    fatigue +=result
            del test
            if num > 0:
                fatigue /= num
            else:
                fatigue = -1
            print(fatigue)
            public.temp_file.save("FATIGUE",{"fatigue":fatigue})
            time.sleep(10)
        except:
            print("ERR")
            del test
    
if __name__ == '__main__':
    run()

