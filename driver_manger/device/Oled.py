import time,public
from PIL import Image
from PIL import ImageDraw, ImageFont
from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106



class Oled():

    def __init__(self):
        self.serial = i2c(port=1, address=0x3C)
        self.device = ssd1306(self.serial)
        self.chinese_font = ImageFont.truetype('NotoSansSC-Regular.ttf', 17)
        
    def show(self,data):
        data.append("");data.append("");data.append("");data.append("");
        #while True:
        with canvas(self.device) as draw:
            #line = 
            #draw.rectangle(device.bounding_box, outline="white", fill="black")
            draw.text((0, 0), data[0],fill="white",font=self.chinese_font)
            draw.text((0, 15), data[1],fill="white",font=self.chinese_font)
            draw.text((0, 30), data[2],fill="white",font=self.chinese_font)
            draw.text((0, 45), data[3],fill="white",font=self.chinese_font)

def run():
    old = None
    while True:
        try:
            new = public.temp_file.read("DISPLAY")
            if old != new:
                test.show(new)
                old = new
        except:
            test = Oled()
        finally:
            time.sleep(0.25)
    
    
if __name__=="__main__":
    run()
    #test.show(["--系统状态--",""," 运行正常!"])