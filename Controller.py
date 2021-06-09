import cv2
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
from Actions.Dance import Dance

# import all components
from Component.Remote import Remote
from Component.Camera import Camera
from Component.Engine import Engine
from Component.Light import Light
from Component.Magnet import Magnet
from Component.Microphone import Microphone
from Component.Servo import Servo
from Component.Weight import Weight
from Component.Sound import Sound


class Controller:
    """
        Controller handles all actions of the robot as a whole.
        It acts as a facade that handles all components
    """

    # initializing all components

    def __init__(self):
        self.__mode = 0

        # make instance of all components with gpio pins as parameters if necessary
        self.__engine2 = Engine(3, 2, 4)
        self.__engine1 = Engine(27, 22, 17)
        self.__servoCamera = Servo(1, 0)
        self.__servoGripper = Servo(0, 1)
        self.__microphone = Microphone()
        self.__light = Light(13)
        self.__camera = Camera()
        self.__magnet = Magnet(16)
        self.__remote = Remote()
        self.__weight = Weight()
        self.__sound = Sound()

        self.__utils = Utils()
        self.__driver = MoveInstructions(self.__servoGripper, self.__servoCamera, self.__magnet, self.__engine1, self.__engine2)
        self.__remoteSocket = RemoteSocket()
        self.__followColor = FollowColor(self.__camera, self.__utils, self.__driver)
       
        # listen to remote on different thread
        # keep update frame in Camera on different thread
        threading.Thread(target=self.__camera.update).start()
        threading.Thread(target=self.__remoteSocket.listen).start()
        threading.Thread(target=self.startRobot).start()
        time.sleep(2)

    # function for listening to the remote with joysticks
    def startRobot(self):
        print("start listening to controller")
        cameraOn = False
        lastTimeReceived = datetime.datetime.now()
        while True:
            print("listening")

            command = self.__remoteSocket.getCommand()
            self.__remoteSocket.clearCommand()
            
            if command is None:
                if datetime.datetime.now() - lastTimeReceived == datetime.timedelta(microseconds = 500000):
                    command = [0]
            else:
                val = list(map(int, command))
                # set joypositions
                print(val)
            
            if self.__mode != val[0]:
                self.__mode = val[0]
                if cameraOn == True:
                    self.cameraOn = False
                    self.__camera.closeVideo()
                    cv2.destroyAllWindows()

            # mode 0 = sleep
            if val[0] == 0:
                self.__driver.move(0, 0)
                self.__driver.moveGripper(0)
                time.sleep(0.5)
                continue
            self.__remote.setJoyPositions([val[1], val[2], val[3], val[4]])

            # mode 1 = drive
            if self.__mode == 1:
                input1 = self.__remote.getPosition('y1')
                input2 = self.__remote.getPosition('y2')
                self.__driver.moveTrackControl(input1, input2)
                continue

            # mode 2 = move gripper
            if self.__mode == 2:
                y1 = self.__remote.getPosition('y1')
                self.__driver.moveGripper(y1, val[5])
                time.sleep(0.05)
                continue

            # mode 3 = following blue car
            if self.__mode == 3:
                if cameraOn != True:
                    cameraOn = True
                self.followColor()
                continue

    # function for following the car with the blue block
    def followColor(self):
        try:
            self.__driver.moveCamera(200)
            followColor = FollowColor(self.__camera, self.__utils, self.__driver)
            followColor.run()
        except:
            pass

    # function to follow the black line
    def followLine(self):
        self.__driver.moveCamera(450)
        followLine = FollowLine(self.__camera, self.__utils, self.__driver)
        followLine.run()

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
    # used in Main where the API endpoint is
    def getComponents(self):
        return self.__camera, self.__microphone
        # return self.__camera, self.__servoGripper, self.__servoCamera, self.__light, self.__engine1, self.__engine2, self.__microphone, self.__weight
