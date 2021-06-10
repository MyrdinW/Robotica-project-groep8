class MoveInstructions:
    def __init__(self, servoGripper, servoCamera, magnet, engine1, engine2):
        self.__servoGripper = servoGripper
        self.__servoCamera = servoCamera
        self.__magnet = magnet
        self.__engine1 = engine1
        self.__engine2 = engine2

        # Moves gripper with x and y value of joystick

    def moveGripper(self, joypos):
        try:
            self.__servoGripper.moveUnlimited(joypos)
        except:
            print("moving gripper failed")

    def moveCamera(self, position):
        self.__servoCamera.moveSpeed(position, 500)
    

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
        self.__engine1.setValue(lefttrack)
        self.__engine2.setValue(righttrack)
        #except:
        #    print("moving robot failed(trackcontrol)")

    def powerMagnet(self, value):
        self.__magnet.switch(value)