import AX12

class Servo:
    """
    Servo initializes all servo properties and utilizes the functions in need for the servo movement for the camera and 
    the arm. 
    In order to move the servo's the AX12 library is used to make the connection and basic moving functions
    The move function moves the servo to a given position (Work in Progress into a loop which will move the camera
    according to joystick position)
    The move_speed function moves the servo to a given position at a given speed (Work in Progress: needs joystick
    implementation aswell)
    The move_unlimited is the function used for the arm, which moves in Wheel Mode and moves according to the joystick position
    """

    
    def __init__(self, id, mode):
        self.__servos = AX12.Ax12()
        self.__id = id

    # Moving the camera servo to a given position between the Angle limits
    def move(self, position):
        self.__servos.move(self.__id, position)
        self.__servos.action()

    # Moving the camera servo to a given position at a given speed between the Angle limits
    def move_speed(self, position, speed):
        self.__servos.moveSpeed(self.__id, position, speed)
        self.__servos.action()
    
    # Moving the arm servo at a given speed/direction according to joystick position (0-1023 is speed CW, 1024-2047 is speed CCW)
    def move_unlimited(self, speed):
        if speed < 0:
            value = int(speed * -1023)
            print(value)
            self.__servos.moveInWheelMode(self.__id, value)
            return
        if speed > 0:
            value = int((speed * 1023) + 1024)
            print(value)
            self.__servos.moveInWheelMode(self.__id, value)
            return
        self.__servos.moveInWheelMode(self.__id, 0)
        