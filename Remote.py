class Remote:
    def __init__(self):
        self.__positions = [0, 0, 0, 0] # 0 = x1, 1 = y1, 2 = x2, 3 = y2  // 0 - 4016 
        self.__deadzone = [0, 2040, 2060, 4016],[0, 2040, 2060, 4016],[0, 2040, 2060, 4016],[0, 2040, 2060, 4016]

    def set_joy_positions(self, positions):
        self.__positions = [positions[0], positions[1], positions[2], positions[3]]

    def calc_value(self, axis_int):
        value = self.__positions[axis_int]
        if value >= 0 and value < self.__deadzone[axis_int][0]:
            return -1

        if value < self.__deadzone[axis_int][1]:
            range = self.__deadzone[axis_int][1] - self.__deadzone[axis_int][0]
            return (value - self.__deadzone[axis_int][1]) / range

        if value < self.__deadzone[axis_int][2]:
            return 0

        if value < self.__deadzone[axis_int][3]:
            range = self.__deadzone[axis_int][3] - self.__deadzone[axis_int][2]
            return (value - self.__deadzone[axis_int][2]) / range

        if value < 4016:
            return 1

    def get_move_positions_track_control(self):
        lefttrack = self.calc_value(1)
        righttrack = self.calc_value(3)
        return [lefttrack, righttrack]

    def get_joy_positions(self):
        return self.__positions


