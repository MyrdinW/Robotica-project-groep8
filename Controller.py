import datetime
import threading
import time

from Camera import Camera
from Engine import Engine
from Remote import Remote
from Light import Light
from Microphone import Microphone
from Receiver import Receiver
from Servo import Servo
from Weight import Weight
from Utils import *

from Weight_fake import Weight_fake
from LaptopReceiver import LaptopReceiver




class Controller:
    """
        Controller handles all actions of the robot as a whole.
        It acts as a facade that handles all components
    """

    def __init__(self):
        self.__task = False
        self.__engine1 = Engine(3, 4, 2)
        self.__engine2 = Engine(27, 17, 22)
        self.__servo = Servo()
        self.__microphone = Microphone()
        self.__light = Light(15)
        self.__camera = Camera()
        self.__Remote = Remote()
        self.__LaptopReceiver = LaptopReceiver()
        try:
            self.__weight = Weight()
        except:
            print("weight failed")
        #self.__receiver = Receiver()
        #threading.Thread(target=self.listen).start()
        threading.Thread(target=self.listentolaptop).start()
        print("controller")
        #threading.Thread(target=self.dance).start()
        #self.__engine.set_value(0.1)
        
        

    # Listens for command from the remote
    def listen(self):
        while True:
            command = self.__receiver.listen()
            if command is not None:
                val = command.split()
                self.__Remote.set_joy_positions([val[1], val[2], val[3], val[4]])
                if val[0] == "move":
                    self.move_track_control(Remote.get_move_positions_track_control())
                    #self.move(Remote.get_move_positions)
                    
                elif val[0] == "movegripper":
                    self.movegripper(val[1], val[2])

    def listentolaptop(self):
        while True:
            response = self.__LaptopReceiver.listen()
            if response is not None:
                self.move(response[0], response[1])





    # Moves gripper with x and y value of joystick
    def movegripper(self, x, y):
        print("Moving gripper")

    # Moves robot with x and y value of joystick
    def move(self, speed, direction):
        self.__engine1.set_value(speed + direction)
        self.__engine2.set_value(speed - direction)

    def move_track_control(self, lefttrack, righttrack):
        self.__engine1.set_value(lefttrack)
        self.__engine2.set_value(righttrack)
        

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
        return self.__camera, self.__servo, self.__light, self.__engine1, self.__engine1, self.__microphone, self.__weight
