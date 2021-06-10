class FollowColor:
    def __init__(self, camera, utils, driver):
        self.__camera = camera
        self.__utils = utils
        self.__driver = driver
        pass

    def run(self):
        # try:
        #time0 = datetime.datetime.now()
        frame = self.__camera.getImage()
        output = self.__utils.getDistanceBlue(frame, 0)
        #print(datetime.datetime.now() - time0)
        print(output)

        #if nothing is detected do nothing is stopping robot
        if not output:
            self.__driver.move(0, 0)
            return

        #if the blue block is in the middle do nothing
        if output[1] < 100:
            self.__driver.move(0, 0)
            return

        #if the blue block is on the left turn left
        if output[0] == "left":
            print("going left")
            turningspeed = output[1]/-255
            self.__driver.move(0, turningspeed)
            return

        #if the blue block is on the left turn right
        elif output[0] == "right":
            print("going right")
            turningspeed = output[1]/255
            self.__driver.move(0, turningspeed)
            return
        # except:
            #print("following line failed")