import datetime
import time

class DanceMoves:
    def __init__(self, driver):
        self.__driver = driver

    def pirouette(self, part, dir): # 1 quarter, 2 half, 4 whole
        if dir == 1:
            self.__driver.move(-1, 1)
        else:
            self.__driver.move(1, -1)
        self.waitforseconds(part * (8/4))
        self.__driver.move(0,0)

    def headbang(self):
        self.__driver.moveCameraMax(0)
        time.sleep(0.5)
        self.__driver.moveCameraMax(1000)
        time.sleep(0.5)

    def updown(self):
        # self.__driver.moveCameraMax()
        pass

    def unknown(self):
        # do left side
        self.__driver.move(1, 2)
        self.waitforseconds(3)
        self.__driver.move(-1, -2)
        self.waitforseconds(6)
        self.__driver.move(1, 2)
        self.waitforseconds(3)

        # do right side
        self.__driver.move(2, 1)
        self.waitforseconds(3)
        self.__driver.move(-2, -1)
        self.waitforseconds(6)
        self.__driver.move(2, 1)
        self.waitforseconds(3)

        # finished
        self.__driver.move(0,0)

    def waitforseconds(self, time):
        timenow = datetime.datetime.now()
        timedif = datetime.timedelta(seconds=time)
        while datetime.datetime.now() < timenow + timedif:
            pass
