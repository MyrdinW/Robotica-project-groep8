import datetime
import time

class DanceMoves:
    def __init__(self, driver):
        self.__driver = driver
        self.__secondbpm = 120 /120

    def pirouette(self, part, dir, stopped): # 1 quarter, 2 half, 4 whole
        if not stopped:
            if dir == 1:
                self.__driver.moveTrackControl(-1, 1)
            else:
                self.__driver.moveTrackControl(1, -1)
            self.waitforseconds(part * (8/4))
            self.__driver.moveTrackControl(0,0)

    def turn(self, dir, duration, stopped):
        if not stopped:
            if dir == 1:
                self.__driver.moveTrackControl(-0.85, 0.85)
            else:
                self.__driver.moveTrackControl(0.85, -0.85)

            self.waitforseconds(duration)
            self.__driver.moveTrackControl(0,0)

    def bocht(self, dir, duration, stopped):
        if not stopped:
            if dir == 1:
              self.__driver.moveTrackControl(-0.2, -1)
            else:
              self.__driver.moveTrackControl(-1, -0.20)

            self.waitforseconds(duration / 2)

            if dir == 0:
              self.__driver.moveTrackControl(0.20, 1)
            else:
              self.__driver.moveTrackControl(1, 0.20)

            self.waitforseconds(duration / 2)
            self.__driver.moveTrackControl(0,0)


    def cross(self, stopped):
        if not stopped:
            for x in range(4):
                self.__driver.moveTrackControl(-1, 1)
                self.waitforseconds(0.5)
                self.__driver.moveTrackControl(1, 1)
                self.waitforseconds(0.5)
                self.__driver.moveTrackControl(-1, -1)
                self.waitforseconds(0.5)

    def headbang(self, stopped):
        if not stopped:
            self.__driver.moveCameraMax(0)
            self.waitforseconds(0.5)
            self.__driver.moveCameraMax(1000)
            self.waitforseconds(0.5)

    def updown(self, stopped):
        if not stopped:
            self.__driver.moveTrackControl(0.9, 0.9)
            print("Moving Forwardstest")
            self.waitforseconds(self.__secondbpm)
            self.__driver.moveTrackControl(-0.9, -0.9)
            print("Moving Backwards")
            self.waitforseconds(self.__secondbpm)
            self.__driver.moveTrackControl(0.9, 0.9)
            print("Moving Forwardstest")
            self.waitforseconds(self.__secondbpm)
            self.__driver.moveTrackControl(-0.9, -0.9)
            print("Moving Backwards")
            self.waitforseconds(self.__secondbpm)
            self.__driver.moveTrackControl(0, 0)

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
            self.__driver.moveTrackControl(-0.9, 0.9)
            self.waitforseconds(1)
            self.__driver.moveTrackControl(0.9, -0.9)
            self.waitforseconds(1)
            self.__driver.moveTrackControl(-0.9, 0.9)
            self.waitforseconds(1)
            self.__driver.moveTrackControl(0.9, -0.9)
            self.waitforseconds(1)
            self.__driver.moveTrackControl(0, 0)

    def waitforseconds(self, time):
        timenow = datetime.datetime.now()
        timedif = datetime.timedelta(seconds=time)
        while datetime.datetime.now() < timenow + timedif:
            pass
