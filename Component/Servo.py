import AX12

class Servo:
    """
    Servo handles all actions of the servos like moving
    """
    def __init__(self, id, mode):
        self.__servos = AX12.Ax12()
        self.__id = id

    # starting positions per action:
    # gate : 550
    # follow line : 450
    # follow block : 224
    # move to position with max speed
    def move(self, position):
        self.__servos.move(self.__id, position)
        self.__servos.action()

    # move with position and speed as parameters
    def moveSpeed(self, position, speed):
        self.__servos.moveSpeed(self.__id, position, speed)
        self.__servos.action()

    # moves arm in wheel mode to a direction
    def moveUnlimited(self, speed):
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
