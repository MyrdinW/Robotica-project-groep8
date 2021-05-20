from Camera import Camera
from Engine import Engine
from Light import Light
from Microphone import Microphone
from Receiver import Receiver
from Remote import Remote
from Servo import Servo
from Weight import Weight
import threading
import time
import RPi.GPIO as gpio
import datetime

class Controller:
    def __init__(self):

    
        self.task = False
        self.remote = Remote()
        self.engine = Engine(3,2,4)
        self.servo = Servo()

        self.microphone = Microphone()

        self.light = Light()
        
        self.camera = Camera()
        # self.camera = None
        print("succeed")
        self.weight = Weight()
        print("Starting listener")
        self.receiver = Receiver(self.camera, self.microphone)
        threading.Thread(target=self.listen).start()
        threading.Thread(target=self.dance).start()
    
    def listen(self):
        while True:
            command = self.receiver.listen()
            if command is not None:
                words = command.split()
                if words[0] == "move":
                    self.move(words[1], words[2])
                elif words[0] == "movegripper":
                    self.movegripper(words[1], words[2])
            time.sleep(0.1)
    
    def movegripper(self, jsx1, jsy1):
        print("Moving gripper")
    
    def move(self, jsx1, jsy1):
        print("movecommand:",jsx1,jsy1)
        value = (int(jsx1) - 2048)/2048
        if value < -0.02 and value > -0.06:
            value = 0
        print(value)
        self.engine.set_value(value)
        self.stop = False
    
    def dance(self):
        print("mic started")
        timedelta = datetime.timedelta(seconds=10)
        timeend = datetime.datetime.now() + timedelta
        while datetime.datetime.now() < timeend:
            low, mid, high = self.microphone.get_maxlights()
            self.light.set_values(low, mid, high)
        self.light.reset_lights()
        print("mic stopped")
    
    def get_components(self):
        return self.camera, self.servo, self.remote, self.light, self.engine, self.microphone, self.weight
