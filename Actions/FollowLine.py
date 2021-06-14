class FollowLine:
    def __init__(self, camera, utils, driver):
        self.__camera = camera
        self.__utils = utils
        self.__driver = driver

    def run(self):
    
        frame = self.__camera.getImage()
        print(frame)
        output = self.__utils.getDistanceBlue(frame, 1)
        
        if not output:
            self.__driver.move(0, 0)
            return
        elif output[2] == True:
            self.__driver.move(0, 0)
            return
        if output[1] < 150:
            self.__driver.move(0.3, 0.0)
            print("moving forward")
            return
        print(output)
        if output[0] == "left":
            print("going left")
            turningspeed = (output[1]-150)/52.5 + 0.5
            self.__driver.moveTrackControl(0, turningspeed)
            return
        if output[0] == "right":
            print("going right")
            turningspeed = (output[1]-150)/52.5 + 0.5
            self.__driver.moveTrackControl(turningspeed, 0)
            return
        self.__driver.move(0, 0)
