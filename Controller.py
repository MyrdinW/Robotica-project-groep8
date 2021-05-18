# Import necessary libraries
from Camera import Camera
from Engine import Engine
from Light import Light
from Microphone import Microphone
from Remote import Remote
from Servo import Servo
from Weight import Weight


class Controller:
    def __init__(self):
        self.task = False
        self.remote = Remote()
        self.engine = Engine()
        self.servo = Servo()
        self.microphone = Microphone()
        self.light = Light()
        self.camera = Camera()
        self.weight = Weight()

    def get_components(self):
        return self.camera, self.servo, self.remote, self.light, self.engine, self.microphone, self.weight
