#! /usr/bin/python3

import json

class temp_file():
    PATH = "/tmp/"
    @staticmethod
    def read(fileName:str):
        try:
            with open(temp_file.PATH + fileName, "r") as f:
                return json.loads(f.read())
        except:
            return None
    @staticmethod
    def save(fileName:str,data):
        try:
            with open(temp_file.PATH+fileName,"w") as f:
                f.write(json.dumps(data))
            return True
        except:
            return False


if __name__ == "__main__":
    print("test code!")
    temp_file.save("tempFile",{"abc":"def"})
    data = temp_file.read("tempFile")
    print(data)
    