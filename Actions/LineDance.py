from Actions.DanceMoves import DanceMoves
import time

class LineDance:

    def __init__(self, microphone, light, lightController, driver):
        self.__microphone = microphone
        self.__light = light
        self.__lightController = lightController
        self.__driver = driver
        self.__danceMoves = DanceMoves(self.__driver)
        self.__counter = 0
        self.__counterTwo = 0
        self.__counterThree = 0
        self.__backwards = False

    def getMovement(self, i):
        #when low leds not 4, don't drive
        if i < 4:
            self.__driver.moveTrackControl(0, 0)
            self.__driver.moveGripper(0)
        #when low leds 4 or higher, do something
        if i >= 4:
            self.__lightController.fireEffect.spark()
            #every 4 times forward/backward switch and after 4 times forward switch to turning sidewards
            if self.__counter <= 0:
                self.__backwards = False
            elif self.__counter >= 4:
                self.__backwards = True
                self.__counterTwo += 1

            if self.__backwards == False:
                if self.__counterTwo == 4:
                    self.__driver.moveTrackControl(-0.8, 0.8)
                    self.__driver.moveCamera(450)
                    print("Dans opzij")
                    time.sleep(0.25)
                    self.__driver.moveTrackControl(0, 0)
                    self.__counterTwo += 1

                elif self.__counterTwo == 5:
                    self.__driver.moveTrackControl(0.8, -0.8)
                    self.__driver.moveCamera(200)
                    print("Dans opzij andere kant")
                    time.sleep(0.25)
                    self.__driver.moveTrackControl(0, 0)
                    self.__counterTwo -= 1
                    self.__counterThree += 1

                    #reset all counters when counterThree gets to 8
                    if self.__counterThree == 8:
                        self.__counter = 0
                        self.__counterTwo = 0
                        self.__counterThree = 0
                else:
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
        low, mid, high = self.__microphone.getMaxLights()
        self.__light.setValues(low, mid, high)
        self.__lightController.fireEffect.cycle()
        self.getMovement((low))

