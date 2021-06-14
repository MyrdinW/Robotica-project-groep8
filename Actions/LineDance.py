import datetime

class LineDance:
    
    def __init__(self, microphone, light, driver):
        self.__microphone = microphone
        self.__light = light
        self.__driver = driver

    def getMovement(self,i,x,y):
        if i >= 4:
            if x >= 0 and y >= 0:
                self.__driver.move(-1, 1)
                print("moving to the back")

            elif x >= 0 and y < 0:
                self.__driver.moveTrackControls(0, 1)
                print("moving to the left")

            elif x < 0 and y >= 0:
                self.__driver.moveTrackControls(1, 0)
                print("moving to the right")

            else:
                self.__driver.move(1, 1)
                print("moving forward")

    def cameraBang(self):
        self.__driver.moveCameraMax(0)
        self.__driver.moveCameraMax(1000)

    def run(self):
        print("dance started")
        timeDelta = datetime.timedelta(minutes=2)
        timeEnd = datetime.datetime.now() + timeDelta
        #while datetime.datetime.now() < timeEnd:
        low, mid, high = self.__microphone.getMaxLights()
        self.__light.setValues(low, mid, high)
        self.getMovement(low, 0, 0)
        self.__light.resetLights()
        print("mic stopped")

