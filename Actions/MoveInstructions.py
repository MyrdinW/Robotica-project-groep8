class MoveInstructions:
    def __init__(self, servoGripper, servoCamera, magnet, engine1, engine2):
        self.__servoGripper = servoGripper
        self.__servoCamera = servoCamera
        self.__magnet = magnet
        self.__engine1 = engine1
        self.__engine2 = engine2

        # Moves gripper with x and y value of joystick

    def moveGripper(self, joypos, magnet = None):
        try:
            self.__servoGripper.moveUnlimited(joypos)
            if magnet is not None:
                self.__magnet.switch(magnet)
        except:
            print("moving gripper failed")

    # move camera with 1/2 speed
    def moveCamera(self, position):
        self.__servoCamera.moveSpeed(position, 500)

# m    # move camera max speed
    def moveCameraMax(self, position):
        self.__servoCamera.move(position)

    # Moves robot with x and y value of joystick
    def move(self, speed, direction):
        try:
            self.__engine1.setValue(speed + direction)
            self.__engine2.setValue(speed - direction)
        except:
            print("moving robot failed(move)")
            self.__engine1.setValue(0)
            self.__engine2.setValue(0)

    def moveTrackControl(self, lefttrack, righttrack):
        #try:
        print(str(lefttrack) + " " + str(righttrack))
        self.__engine1.setValue(lefttrack)
        self.__engine2.setValue(righttrack)
        #except:
        #    print("moving robot failed(trackcontrol)")
