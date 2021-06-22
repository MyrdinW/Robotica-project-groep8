import datetime
from Actions.DanceMoves import DanceMoves
import time


class LineDance:


    def __init__(self, microphone, light, driver):
        self.__microphone = microphone
        self.__light = light
        self.__driver = driver
        self.__danceMoves = DanceMoves(self.__driver)
        self.__counter = 0
        self.__backwards = False

    # def doMove(self):
    #     if self.__move == 0:
    #         self.__danceMoves.pirouette(4, 1)
    #     elif self.__move == 1:
    #         self.__danceMoves.unknown()
    #     elif self.__move == 2:
    #         pass

    def getMovement(self, i):
        if i < 4:
            self.__driver.move(0, 0)
            self.__driver.moveGripper(0)
        if i >= 4:
            if self.__counter <= 0:
                self.__backwards = False
            elif self.__counter >= 4:
                self.__backwards = True

            if self.__backwards == False:
                self.__driver.moveTrackControl(0.4, 0.4)
                self.__driver.moveCamera(450)
                time.sleep(0.15)
                self.__driver.moveTrackControl(0, 0)
                print("Dans naar voren")
                self.__counter += 1
                
            elif self.__backwards == True:
                self.__driver.moveTrackControl(-0.4, -0.4)
                self.__driver.moveCamera(200)
                time.sleep(0.15)
                self.__driver.moveTrackControl(0, 0)
                print("Dans naar achter")
                self.__counter -= 1               
            print(self.__counter)

    def run(self):
        #print("dance started")
        timeDelta = datetime.timedelta(minutes=2)
        timeEnd = datetime.datetime.now() + timeDelta
        # while datetime.datetime.now() < timeEnd:
        low, mid, high = self.__microphone.getMaxLights()
        # low = 1
        # mid = 1
        # high = 1
        self.__light.setValues(low, mid, high)
        self.getMovement((low))
        #self.doMove()
        # self.__danceMoves.headbang()
        #print("line dance iteration")
