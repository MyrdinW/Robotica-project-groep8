class Servo:
    def __init__(self):
        self.torque = 0
        self.value = 0

    def set_value(self, value):
        self.value =value

    def get_value(self):
        return self.value

    def set_torque(self, torque):
        self.torque = torque

    def get_torque(self):
        return self.torque
