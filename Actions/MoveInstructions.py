class MoveInstructions:
    """
    MoveInstructions handles the movements the robot does.
    It sends signals to the servos and engines
    """
    def __init__(self, servoGripper, servoCamera, magnet, engine1, engine2):
        self.__servoGripper = servoGripper
        self.__servoCamera = servoCamera
        self.__magnet = magnet
        self.__engine1 = engine1
        self.__engine2 = engine2

    # moves gripper with x and y value of joystick
    def moveGripper(self, joypos, magnet = None):
        try:
            self.__servoGripper.moveUnlimited(joypos)
            if magnet is not None:
                self.__magnet.switch(magnet)
        except:
            print("moving gripper failed")

    # moves camera to a position with speed 500
    def moveCamera(self, position):
        self.__servoCamera.moveSpeed(position, 500)
    

    # moves robot with x and y value of joystick
    def move(self, speed, direction):
        try:
            self.__engine1.setValue(speed + direction)
            self.__engine2.setValue(speed - direction)
        except:
            print("moving robot failed(move)")
            self.__engine1.setValue(0)
            self.__engine2.setValue(0)

    # change the positions of the tracks, used when turning
    def moveTrackControl(self, lefttrack, righttrack):
        self.__engine1.setValue(lefttrack)
        self.__engine2.setValue(righttrack)
