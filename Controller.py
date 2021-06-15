import threading
import time
import cv2
from Actions.Dance import Dance
from Actions.FollowColor import FollowColor
from Actions.FollowLine import FollowLine
from Actions.LineDance import LineDance
from Actions.Mask import Mask
# import Action classes
from Actions.MoveInstructions import MoveInstructions
from Component.Camera import Camera
from Component.Engine import Engine
from Component.Light import Light
from Component.Magnet import Magnet
from Component.Microphone import Microphone
# import all components
from Component.Remote import Remote
from Component.Servo import Servo
from Component.Weight import Weight
from Connections.RemoteSocket import RemoteSocket
from Utils import Utils


# import class that handles movements
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
        self.__followColor = FollowColor(self.__camera, self.__utils, self.__driver)
        self.__followLine = FollowLine(self.__camera, self.__utils, self.__driver)
        self.__mask = Mask(self.__camera, self.__utils, self.__driver, self.__light)
        self.__lineDance = LineDance(self.__microphone, self.__light, self.__driver)

        # listen to remote on different thread
        # keep update frame in Camera on different thread
        threading.Thread(target=self.__camera.update).start()
        time.sleep(3)
        threading.Thread(target=self.__remoteSocket.listen).start()
        threading.Thread(target=self.startRobot).start()
        threading.Thread(target=self.__weight.update()).start()
       
    # function for listening to the controller
    def startRobot(self):
        print("start listening to controller")
        # thread = None
        counter = 0
        while True:
            self.__command = self.__remoteSocket.getCommand()
            self.__remoteSocket.clearCommand()

            if self.__command is None:
                counter += 1
                if counter == 20:
                    print("lagging")
                    self.__driver.move(0, 0)
                    self.__driver.moveGripper(0)

                time.sleep(0.01)
                continue 
            

            #print(delta)
            counter = 0

            if self.__mode != self.__command[0]:
                cv2.destroyAllWindows()
                self.__mode = self.__command[0]


            # mode 0 = sleep
            if self.__mode == 0:
                self.__driver.move(0, 0)
                self.__driver.moveGripper(0)
                time.sleep(0.5)
                continue
            
            # mode 1 = drive
            if self.__mode == 1:
                self.moveRobot()
                continue

            # mode 2 = move gripper
            if self.__mode == 2:
                self.moveGripper()
                continue

            # mode 3 = following blue car
            if self.__mode == 3:
                position = self.__servoCamera.getPosition()
                if 190 < position < 210:
                    self.__driver.moveCamera(200)
                self.followCar()
                
                continue

             # mode 4 = following line
            if self.__mode == 4:
                position = self.__servoCamera.getPosition()
                if 440 < position < 460:
                    self.__driver.moveCamera(450)
                self.followLine()
                continue
            
             # mode 5 = mask
            if self.__mode == 5:
                position = self.__servoCamera.getPosition()
                if 540 < position < 560:
                    self.__driver.moveCamera(550)
                self.mask()
                continue
            
            # mode 6 = dance
            if self.__mode == 6:
                #eigen muziek
                #self.dance()
                continue
            
            # mode 7 = linedacne
            if self.__mode == 7:
                self.lineDance()
                continue
            
    #function for moving the robot
    def moveRobot(self):

        try:
            self.__remote.setJoyPositions([self.__command[1], self.__command[2], self.__command[3], self.__command[4]])
            self.__remote.setMagnet(self.__command[5])
            input1 = self.__remote.getPosition('y1')
            input2 = self.__remote.getPosition('y2')
            self.__driver.moveTrackControl(input1, input2)
            #self.__driver.moveGripper(0, self.__remote.getMagnet())
            if input1 != 0 or input2 != 0:
                print("moving robot")
        except:
            print("moving robot failed")



    #function for moving the gripper
    def moveGripper(self):
        try:
            self.__remote.setJoyPositions([self.__command[1], self.__command[2], self.__command[3], self.__command[4]])
            self.__remote.setMagnet(self.__command[5])
            y1 = self.__remote.getPosition('y1')
            y2 = self.__remote.getPosition('y2')
            self.__driver.moveGripper(y1, self.__remote.getMagnet())
            if y1 != 0:
                pass
                # print("moving gripper")
            if 0.9 <= y2 <= 1.0:
                print("moving up")
                self.__driver.moveCamera(self.__servoCamera.getPosition() - 20)
            elif -1.0 <= y2 <= -0.9:
                print("moving down")
                self.__driver.moveCamera(self.__servoCamera.getPosition() + 20)
            time.sleep(0.1)
        except Exception as e:
            #   print(e)
            pass

    
    
    
    # function for folling the car with the blue block
    def followCar(self):
        print("followcar")
        self.__followColor.run()
        # cv2.destroyAllWindows()
    
           
    def followLine(self):
        print("followline")
        self.__followLine.run()
        # cv2.destroyAllWindows()


    # function for detecting is someone wears a mask
    def mask(self):
        print("mask")
        self.__mask.run()
        # cv2.destroyAllWindows()

    # Robot (hardcoded) dance command
    def dance(self):
        dance = Dance()
        #dance.run()

    # Robot (on music interpretated) LineDance command
    def lineDance(self):
        self.__lineDance.run()
        
    # returns all components
    def getComponents(self):
        return self.__camera, self.__servoGripper, self.__light, self.__engine1, self.__engine2, self.__microphone, self.__weight
