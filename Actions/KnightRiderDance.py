import datetime
from Actions.DanceMoves import DanceMoves

class KnightRiderDance:

    def __init__(self, driver, microphone, light):
        self.__microphone = microphone
        self.__driver = driver
        self.__light = light
        self.__dancemoves = DanceMoves(driver)

        self.__light = light
        self.__LedLeft= 38
        self.__LedRight = 54

        self.__led1 = 41
        self.__led2 = 40
        self.__led3 = 39
        self.__led4 = 38
        self.__led5 = 37

        self.__start = 41
        self.__backwards = False
        self.dancing = False
        self.completed = False
        print("Dance initialized")

    def reset(self):
        self.__completed = False

    def startKnightRiderDance(self):
        self.__dancemoves.shuffle(self.__stopped)
        print("Ik doe nu die shuffle")

    def stop(self):
        self.__stopped = True
        self.__driver.moveTrackControl(0,0)
        

# 
#     def cycle(self):
#         output = []
#         if self.__led1 >= self.__LedRight:
#             self.__backwards = True
#         elif self.__led1 <= self.__LedLeft:
#             self.__backwards = False
# 
#         output.append([self.__led5, (0, 10, 0, 0)])
#         output.append([self.__led4, (0, 80, 0, 0)])
#         output.append([self.__led3, (0, 180, 0, 0)])
#         output.append([self.__led2, (0, 220, 0, 0)])
#         output.append([self.__led1, (0, 255, 0, 0)])
# 
#         self.__led5 = self.__led4
#         self.__led4 = self.__led3
#         self.__led3 = self.__led2
#         self.__led2 = self.__led1
#         if self.__backwards == True:
#             self.__led1 -= 1
#         else:
#             self.__led1 += 1
# 
#         self.__light.setLights(output)