import datetime
import threading
import time

from Camera import Camera
from Engine import Engine
from Light import Light
from Microphone import Microphone
from Receiver import Receiver
from Servo import Servo
from Weight import Weight
from Weight_fake import Weight_fake
from Utils import *


class Controller:
    """
        Controller handles all actions of the robot as a whole.
        It acts as a facade that handles all components
    """

    def __init__(self):
        self.__task = False
        self.__engine = Engine(3, 2, 4)
        self.__servo = Servo()
        self.__microphone = Microphone()
        self.__light = Light(15)
        self.__camera = Camera()
        try:
            self.__weight = Weight()
        except:
            print("weight failed")
        self.__receiver = Receiver(self.__camera, self.__microphone)
        threading.Thread(target=self.listen).start()
        print("controller")
        #threading.Thread(target=self.dance).start()
        #self.__engine.set_value(0.1)
        
        

    # Listens for command from the remote
    def listen(self):
        while True:
            command = self.__receiver.listen()
            if command is not None:
                words = command.split()
                if words[0] == "move":
                    self.move(words[1], words[2])
                elif words[0] == "movegripper":
                    self.movegripper(words[1], words[2])
            time.sleep(0.1)
            

    # Moves gripper with x and y value of joystick
    def movegripper(self, x, y):
        print("Moving gripper")

    # Moves robot with x and y value of joystick
    def move(self, speed = 0, direction = 0):
        self.__engine1.set_value(speed + direction)
        self.__engine2.set_value(speed - direction)
        
        
        value = (int(jsx1) - 2048) / 2048
        if -0.02 > value > -0.06:
            value = 0
        self.__engine.set_value(value)

    # Robot dance command
    def dance(self):
        print("dance started")
        timedelta = datetime.timedelta(minutes=100)
        timeend = datetime.datetime.now() + timedelta
        while datetime.datetime.now() < timeend:
            low, mid, high = self.__microphone.get_max_lights()
            self.__light.set_values(low, mid, high)
        self.__light.reset_lights()
        print("mic stopped")

    # returns all components
    def get_components(self):
        return self.__camera, self.__servo, self.__light, self.__engine, self.__microphone, self.__weight
