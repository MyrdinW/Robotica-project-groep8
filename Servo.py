import AX12

class Servo:
    def __init__(self, id, mode):
        self.__servos = AX12.Ax12()
        self.__id = id
        data = open("servo.txt", "r", encoding="utf-8").read().split()
        self.__rotation = data[1]
        self.__llimit = [87, 0]
        self.__hlimit = [563, 1]
        # 87 rotation 0 start
    
    def move_to_weight(self):
        self.__servos.moveInWheelMode(self.__id, 400)
        self.skip = False
        while True:
            position = self.__servos.readPosition(self.__id)
            if position < 87 and self.__rotation == 0:
                self.__servos.moveInWheelMode(self.__id, 0)
                break
            
            
                self.__rotation += 1
            cur_pos = self.__servos.readPosition(self.__id)
            self.save(cur_pos)
        
    
    def move(self, position):
        self.__servos.move(self.__id, position)
        self.__servos.action()

    def move_speed(self, position, speed):
        self.__servos.moveSpeed(self.__id, position, speed)
        self.__servos.action()
    
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
        
        
        
    def save(self, position):
        open("servo.txt", "w").write(position + " " + self.__rotation)


