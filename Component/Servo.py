import AX12

class Servo:
    def __init__(self, id, mode):
        self.__servos = AX12.Ax12()
        self.__id = id
        try:
            self.__position = self.__servos.readPosition(id)
        except:
            self.__position = 250

        # 87 rotation 0 start

    # gate : 550
    # follow line : 450
    # follow block : 224
    def move(self, position):
        self.__servos.move(self.__id, position)
        self.__servos.action()
        time.sleep(1)
        self.__position = position


    def moveSpeed(self, position, speed):
        if position > 550:
            position = 550
        if position < 11 :
            position = 11
        self.__position = position
        self.__servos.moveSpeed(self.__id, position, speed)
        #self.__servos.action()
        time.sleep(1)
        self.__position = self.__servos.readPosition(1)
    
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
    
    def getPosition(self):
        #print(self.__position)
        return self.__position