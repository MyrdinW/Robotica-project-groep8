import datetime
from Actions.DanceMoves import DanceMoves
import threading
import random


class Dance:

    def __init__(self, driver, microphone):
        self.__beats = [4,4,4,4,4,4,4,5,4,6,4,4,6,6,4,4,4,4,4,4,4,4,4,4,4,4,4]
        self.__microphone = microphone
        self.__driver = driver
        self.__left = True
        self.__dancemoves = DanceMoves(driver)
        self.timenow = 0
        self.timedif = 0
        self.dancing = False
        self.completed = False
        print("Dance initialized")

    def reset(self):
        self.completed = False

    def startDance(self):
        for beat in self.__beats:
            print(beat)
            if beat == 4:
                #Move back and forward
                if random.randint(0, 2) == 0:
                    self.__dancemoves.shuffle(self.__stopped)
                else:
                    self.__dancemoves.updown(self.__stopped)
            elif beat == 5:
                self.__dancemoves.turn(0, 5, self.__stopped)
            else:
                self.__dancemoves.bocht(1, 6, self.__stopped)
                
#         self.__dancemoves.pirouette(4, 0, self.__stopped)
#         print("pir")
#         self.__dancemoves.shuffle(self.__stopped)
#         print("shuf")
#         self.__dancemoves.shuffle(self.__stopped)
#         print("shuf")
#         self.__dancemoves.shuffle(self.__stopped)
#         print("shuf")
#         print("Dance: 1 Completed")
#         self.__dancemoves.cross(self.__stopped)
#
#         print("Dance: 2 Completed")
#         self.__dancemoves.pirouette(4, 0, self.__stopped)
#
#         print("Dance: 3 Completed")
#         self.__dancemoves.flutterby(self.__stopped)
#
#         print("Dance: 4 Completed")
#         self.__dancemoves.pirouette(2, 0, self.__stopped)
#
#
#         print("Dance: 5 Completed")
#         self.__dancemoves.pirouette(1, 1, self.__stopped)
#         print("Dance: 6 Completed")
#         self.__dancemoves.pirouette(2, 0, self.__stopped)
#         print("Dance: 7 Completed")
#         self.__dancemoves.pirouette(3, 1, self.__stopped)
#         print("Dance: 8 Completed")
#         self.__dancemoves.flutterby(self.__stopped)
#         print("Dance: 9 Completed")
#         self.__dancemoves.cross(self.__stopped)
#         print("Dance: 10 Completed")
        self.dancing = False
        self.completed = True

    def run(self):
        if not self.completed:
            if self.dancing is False:
                self.dancing = True
                self.__stopped = False
                self.timenow = datetime.datetime.now()
                self.timedif = datetime.timedelta(seconds=2)
                self.__t = threading.Thread(target=self.startDance)
                self.__t.start()
            else:
                pass
            #    self.lights()
             #   self.timenow = datetime.datetime.now()

            #while datetime.datetime.now() < self.timenow + self.timedif:
            #    self.dancing = False
            #    self.completed = True

    def stop(self):
        self.__stopped = True
        self.__driver.moveTrackControl(0,0)

