import playsound
import os
import random


class Sound:
    def __init__(self):
        self.__r2d2 = os.listdir("sounds/r2d2")
        self.__relevant = os.listdir("sounds/makes_sense")
        self.__nsfw = os.listdir("sounds/nsfs")
    
    def random_robot(self):
        # playsound.playsound(f"sounds/rd2d/{random.choice(self.__r2d2)}")
        #os.system(f"mpg321 sounds/rd2d/{random.choice(self.__r2d2)}.mp3")
        # playsound.playsound(f"sounds/r2d2/test.mp3")
        os.system(f"mpg321 sounds/r2d2/integratie.mp3")
    def random_relevant(self):
        playsound.playsound(f"sounds/makes_sense/{random.choice(self.__relevant)}")
    
    def random_nsfs(self):
        playsound.playsound(f"sounds/nsfs/{random.choice(self.__nsfw)}")

sound  = Sound()
sound.random_robot()