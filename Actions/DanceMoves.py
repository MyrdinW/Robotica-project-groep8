import datetime
import time

class DanceMoves:
    def __init__(self, driver):
        self.__driver = driver


    def pirouette(self, part, dir, stopped): # 1 quarter, 2 half, 4 whole
        if not stopped:
            if dir == 1:
                self.__driver.moveTrackControl(-1, 1)
            else:
                self.__driver.moveTrackControl(1, -1)
            self.waitforseconds(part * (8/4))
            self.__driver.moveTrackControl(0,0)

    def cross(self, stopped):
        if not stopped:
            for x in range(4):
                self.__driver.moveTrackControl(-1, 1)
                self.waitforseconds(1)
                self.__driver.moveTrackControl(1, 1)
                self.waitforseconds(2)
                self.__driver.moveTrackControl(-1, -1)
                self.waitforseconds(2)

    def headbang(self, stopped):
        if not stopped:
            self.__driver.moveCameraMax(0)
            self.waitforseconds(0.5)
            self.__driver.moveCameraMax(1000)
            self.waitforseconds(0.5)

    def updown(self):
        # self.__driver.moveCameraMax()
        pass

    def flutterby(self, stopped):
        if not stopped:
            # do left side
            self.__driver.moveTrackControl(1, 2)
            self.waitforseconds(3)
            self.__driver.moveTrackControl(-1, -2)
            self.waitforseconds(6)
            self.__driver.moveTrackControl(1, 2)
            self.waitforseconds(3)

            # do right side
            self.__driver.moveTrackControl(2, 1)
            self.waitforseconds(3)
            self.__driver.moveTrackControl(-2, -1)
            self.waitforseconds(6)
            self.__driver.moveTrackControl(2, 1)
            self.waitforseconds(3)

            # finished
            self.__driver.moveTrackControl(0,0)

    def cirkel(self, stopped):
        if not stopped:
            pass

    def shuffle(self, stopped):
        if not stopped:
            self.__driver.moveTrackControl(-1, 1)
            self.waitforseconds(1)
            self.__driver.moveTrackControl(1, -1)
            self.waitforseconds(1)
            self.__driver.moveTrackControl(-1, 1)
            self.waitforseconds(1)
            self.__driver.moveTrackControl(1, -1)
            self.waitforseconds(1)

    def waitforseconds(self, time):
        timenow = datetime.datetime.now()
        timedif = datetime.timedelta(seconds=time)
        while datetime.datetime.now() < timenow + timedif:
            pass
