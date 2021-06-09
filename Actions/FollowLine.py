class FollowLine:
    """
    FollowLine makes the robot follow the black line on the stairs and elevation
    It uses the class Utils to get the distance to the black line
    """
    def __init__(self, camera, utils, driver):
        self.__camera = camera
        self.__utils = utils
        self.__driver = driver

    # makes the robot follow the black line

    def run(self):
        for i in range(1000):
            frame = self.__camera.getImage()
            output = self.__utils.getDistanceBlue(frame, 1)
            
            if not output:
                self.__driver.move(0, 0)
                continue
            elif output[2] == True:
                self.__driver.move(0, 0)
                continue
            if output[1] < 150:
                self.__driver.move(0.3, 0.0)
                print("moving forward")
                continue
            print(output)
            if output[0] == "left":
                print("going left")
                turningspeed = (output[1]-150)/52.5 + 0.5
                self.__driver.moveTrackControl(0, turningspeed)
                continue
            if output[0] == "right":
                print("going right")
                turningspeed = (output[1]-150)/52.5 + 0.5
                self.__driver.moveTrackControl(turningspeed, 0)
                continue
            self.__driver.move(0, 0)
            # except:
            # print("exception")
        self.__camera.closeVideo()
        # exit()