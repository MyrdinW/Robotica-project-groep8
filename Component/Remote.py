class Remote:
    def __init__(self):
        self.__positions = [0, 0, 0, 0] # 0 = x1, 1 = y1, 2 = x2, 3 = y2  // 0 - 1000
        self.__deadzone = [100, 439, 449, 900],[100, 437, 447, 900],[100, 450, 460, 900],[100, 429, 439, 900]
        self.__magnet = False

    def setJoyPositions(self, positions):
        self.__positions = [positions[0], positions[1], positions[2], positions[3]]

    def setMagnet(self, magnet):
        self.__magnet = magnet

    def calcValue(self, axisInt):
        value = self.__positions[axisInt]
        if value >= 0 and value < self.__deadzone[axisInt][0]:
            return -1

        if value < self.__deadzone[axisInt][1]:
            range = self.__deadzone[axisInt][1] - self.__deadzone[axisInt][0]
            return (value - self.__deadzone[axisInt][1]) / range

        if value < self.__deadzone[axisInt][2]:
            return 0

        if value < self.__deadzone[axisInt][3]:
            range = self.__deadzone[axisInt][3] - self.__deadzone[axisInt][2]
            return (value - self.__deadzone[axisInt][2]) / range

        if value >= self.__deadzone[axisInt][3]:
            return 1

    def getPosition(self, joystick):
        if joystick == 'x1':
            return self.calcValue(0)
        if joystick == 'y1':
            return self.calcValue(1)
        if joystick == 'x2':
            return self.calcValue(2)
        if joystick == 'y2':
            return self.calcValue(3)
        return 0

    def getMagnet(self):
        return self.__magnet
    
    def getJoyPositions(self):
        return self.__positions


