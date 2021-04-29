# Import necessary libraries
from Camera import Camera
from Engine import Engine
from Light import Light
from Microphone import Microphone
from Remote import Remote
from Servo import Servo


class Controller:
    def __init__(self):
        self.task = False
        self.remote = Remote()
        self.engine = Engine()
        self.servo = Servo()
        self.microphone = Microphone()
        self.light = Light()
        self.camera = Camera()

    def move_gripper(self):
        self.task = True
        pass

    def dance(self):
        self.task = True
        pass

    def follow_line(self):
        self.task = True
        pass

    def follow_car(self):
        self.task = True
        pass

    def pickup_mask(self):
        self.task = True
        pass

    def move(self):
        while True:
            if self.remote.moved():
                # robot code to move
                pass

    def abort(self):
        self.task = False

    def get_components(self):
        return self.camera, self.servo, self.remote, self.light, self.engine, self.microphone
