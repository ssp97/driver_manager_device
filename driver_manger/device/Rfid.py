from pirc522 import RFID
import time,public

class Rfid():
    def __init__(self):
        self.rdr = RFID()
    
    def read(self):
          self.rdr.wait_for_tag()
          (error, tag_type) = self.rdr.request()
          if error:
              return None
          if not error:
            #print("Tag detected")
            (error, uid) = self.rdr.anticoll()
            if not error:
              return uid
              # Select Tag is required before Auth
              if not self.rdr.select_tag(uid):
                # Auth for block 10 (block 2 of sector 2) using default shipping key A
                  self.rdr.stop_crypto()

def run():
    #GPIO.setwarnings(False)
    result = []
    test = Rfid()
    while True:
        uid = test.read()
        if uid != None:
            uid = "%02X%02X%02X%02X" % (uid[0],uid[1],uid[2],uid[3])
            print(uid)
            public.temp_file.save("RFID",{"uid":uid,"time":time.time()})
            time.sleep(2)

if __name__ == "__main__":
    run()