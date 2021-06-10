import cv2
import imutils
import threading
import time
import datetime


from Utils import Utils

# import class that handles movements

from Connections.RemoteSocket import RemoteSocket

# import Action classes
from Actions.MoveInstructions import MoveInstructions
from Actions.FollowColor import FollowColor
from Actions.FollowLine import FollowLine
from Actions.Mask import Mask

# import all components
from Component.Remote import Remote
from Component.Camera import Camera
from Component.Engine import Engine
from Component.Light import Light
from Component.Magnet import Magnet
from Component.Microphone import Microphone
from Component.Servo import Servo
from Component.Weight import Weight
# from Component.Sound import Sound


class Controller:
    """
        Controller handles all actions of the robot as a whole.
        It acts as a facade that handles all components
    """

    # initializing all components

    def __init__(self):
        self.__mode = 0

        # self.__sound = Sound()
        self.__engine2 = Engine(3, 2, 4)
        self.__engine1 = Engine(27, 22, 17)
        self.__servoCamera = Servo(1, 0)
        self.__servoGripper = Servo(0, 1)
        self.__microphone = Microphone()
        self.__light = Light(13)
        self.__camera = Camera()
        self.__magnet = Magnet(16)
        self.__utils = Utils()
        self.__remote = Remote()
        self.__remoteSocket = RemoteSocket()
        self.__weight = Weight()
        self.__driver = MoveInstructions(self.__servoGripper, self.__servoCamera, self.__magnet, self.__engine1, self.__engine2)
        
        self.__command = None
       
        

        # listen to remote on different thread
        # keep update frame in Camera on different thread
        threading.Thread(target=self.__camera.update).start()
        threading.Thread(target=self.__remoteSocket.listen).start()
        threading.Thread(target=self.startRobot).start()
       
        

        


    # function for listening to the controller
    def startRobot(self):
        print("start listening to controller")
        thread = None
        while True:
            print("listening")

            self.__command = self.__remoteSocket.getCommand()
            self.__remoteSocket.clearCommand()
        
            if self.__command is None:
                time.sleep(0.05)
                continue 

            #check if mode is the same, if it is continue
            if self.__mode == self.__command[0]:
                time.sleep(0.05)
                continue
            
            #mode is not the same so change mode 
            self.__mode = self.__command[0]

            #if a thread is already running 
            if thread != None:
                thread.join()
            
            # mode 0 = sleep
            if self.__mode == 0:
                self.__driver.move(0, 0)
                self.__driver.moveGripper(0)
                time.sleep(0.5)
                continue

            # mode 1 = drive
            if self.__mode == 1:
                thread = threading.Thread(target=self.moveRobot).start()
                continue

            # mode 2 = move gripper
            if self.__mode == 2:
                thread = threading.Thread(target=self.moveGripper).start()
                continue

            # mode 3 = following blue car
            if self.__mode == 3:
                thread = threading.Thread(target=self.followCar).start()
                continue

             # mode 3 = following line
            if self.__mode == 3:
                thread = threading.Thread(target=self.followLine).start()
                continue

    #function for moving the robot
    def moveRobot(self):
        print("moverobot")
        while self.__mode == 1:
            self.__remote.setJoyPositions([self.__command[1], self.__command[2], self.__command[3], self.__command[4]])
            input1 = self.__remote.getPosition('y1')
            input2 = self.__remote.getPosition('y2')
            self.__driver.moveTrackControl(input1, input2)
            if input1 != 0 or input2 != 0:
                print("moving robot")
        self.__driver.moveTrackControl(0, 0)

    #function for moving the gripper
    def moveGripper(self):
        print("movegripper")
        while self.__mode == 2:
            self.__remote.setJoyPositions([self.__command[1], self.__command[2], self.__command[3], self.__command[4]])
            self.__remote.setMagnet(self.__command[5])
            y1 = self.__remote.getPosition('y1')
            self.__driver.moveGripper(y1, self.__remote.getMagnet())
            if y1 != 0:
                print("moving gripper")
        self.__driver.moveGripper(0, 0)


    # function for folling the car with the blue block
    def followCar(self):
        print("followcar")
        self.__driver.moveCamera(200)
        followColor = FollowColor(self.__camera, self.__utils, self.__driver)
        while self.__mode == 3:
            followColor.run()
        self.__camera.closeVideo()
        cv2.destroyAllWindows()
    

           
    def followLine(self):
        print("followline")
        self.__driver.moveCamera(450)
        followLine = FollowLine(self.__camera, self.__utils, self.__driver)
        while self.__mode == 4:
            followLine.run()
        self.__camera.closeVideo()
        cv2.destroyAllWindows()


    # function for detecting is someone wears a mask
    def mask(self):
        self.__driver.moveCamera(550)
        mask = Mask(self.__camera, self.__utils, self.__driver)
        mask.run()

    # Robot dance command
    def dance(self):
        dance = Dance(self.__microphone, self.__light)
        dance.run()

    # returns all components
    def getComponents(self):
        return self.__camera, self.__servoGripper, self.__light, self.__engine1, self.__engine2, self.__microphone, self.__weight
