import datetime
import threading
import time
import imutils
from Camera import Camera
from Engine import Engine
from Remote import Remote
from Light import Light
from Microphone import Microphone
from Receiver import Receiver
from Servo import Servo
from Weight import Weight
from Magnet import Magnet
from Utils import Utils
#from Sound import Sound
import cv2
from RemoteSocket import RemoteSocket

class Controller:
    """
        Controller handles all actions of the robot as a whole.
        It acts as a facade that handles all components
    """

    #initializing all components 

    def __init__(self):
        self.__mode = 0
        #self.__sound = Sound()
        self.__engine1 = Engine(3, 4, 2)
        self.__engine2 = Engine(27, 17, 22)
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

        threading.Thread(target=self.remoteListener).start()
       


        #
        cameraOn = False
        while True:
            while self.__mode == 3:
                cameraOn = True
                self.followCollor(False, 0)
            if cameraOn == True:
                cameraOn = False
                self.__camera.closeVideo()
                cv2.destroyAllWindows()


    #function for listening to the controller
    def remoteListener(self):
        print("start listening to controller")
        lastTimeReceived = datetime.datetime.now()
        while True:
            command = self.__RemoteSocket.listen()
            
            if command is None:
                if datetime.datetime.now() - lastTimeReceived = datetime.timedelta(microseconds = 500000):
                    command = [0]
                else:
                    continue
            else:
                val = list(map(int, command))

            lastTimeReceived = datetime.datetime.now()
                
                        
            #mode 0 = sleep
            print(val)
            if val[0] == 0:
                if self.__mode != 0:
                    self.__mode = 0
                self.move(0, 0)
                self.moveGripper(0)
                continue
                
            #set joypositions
            self.__remote.setJoyPositions([val[1], val[2], val[3], val[4]])

            #mode 1 = drive
            if val[0] == 1:
                if self.__mode != 1:
                    self.__mode = 1
               
                input1 = self.__remote.getPosition('y1')
                input2 = self.__remote.getPosition('y2')
                
                #self.move_track_control(y1, y2)
                self.moveTrackControl(input1, input2)
            
            #mode 2 = move gripper
            if val[0] == 2:
                if self.__mode != 2:
                    self.__mode = 2
                y1 = self.__remote.getPosition('y1')
                print(y1)
                self.moveGripper(y1, val[5])
                continue
            
            #mode 3 = following blue car 
            if val[0] == 3:
                if self.__mode != 3:
                    self.__mode = 3
                continue



                    
    #Function for following the line on the staircase 
    def followLine(self ):
        for i in range(1000):
            frame = self.__camera.getImage()
            # print(frame)
            # try:
            time0 = datetime.datetime.now()
            output = self.__utils.get_distanceBlue(frame, 1)
            print(datetime.datetime.now() - time0)
            if not output:
                self.move(0, 0)
                continue
            if output[1] < 200:
                self.move(0.3, 0.0)
                print("moving forward")
                continue
            print(output)
            if output[0] == "left":
                print("going left")
                self.moveTrackControl(0.8, 0)
                continue
            if output[0] == "right":
                print("going right")
                self.moveTrackControl(0, 0.8)
                continue
            self.move(0, 0)
            # except:
            # print("exception")
        self.__camera.closeVideo()
        cv2.destroyAllWindows()
        # exit()
        
    
    #function for folling the car with the blue block
    def followCollor(self, driving = False, color):
        try:        
            #time0 = datetime.datetime.now()
            frame = self.__camera.getImage()
            output = self.__utils.getDistanceBlue(frame, color)
            #print(datetime.datetime.now() - time0)
            print(output)
            
            #if nothing is detected do nothing is stopping robot
            if not output:
                self.move(0, 0)
                return 

            #if the blue block is in the middle do nothing
            if output[1] < 50:
                if driving == True:
                    self.move(0.3 , 0)
                else:
                    self.move(0.0 , 0)

            #if the blue block is on the left turn left 
            if output[0] == "left":
                print("going left")
                self.move(0, -0.1)
                return

            #if the blue block is on the left turn right 
            elif output[0] == "right":
                print("going right")
                self.move(0, 0.1)   
                return
        except:
            print("following line failed")

    #function for detecting is someone wears a mask 
    def mask(self):
        # get frame from the video stream and resize it
        for i in range(200):
            frame = self.__camera.getImage()
            frame = imutils.resize(frame, width=800)

            # detect faces in the frame and determine if they are wearing a mask
            try:
                locs, preds = self.__utils.detectAndPredictMask(frame)

                for (box, pred) in zip(locs, preds):
                    (startX, startY, endX, endY) = box
                    (mask, withoutMask) = pred

                    # determine the label and color which are used to draw the box and text
                    label = "Mask" if mask > withoutMask else "No Mask"
                    if mask < withoutMask:
                        print("No mask")
                    else:
                        print("Mask")
                        # threading.Thread(target=playsound.playsound("shall.mp3")).start()

                    # set the color based on the label
                    color = (0, 255, 0) if label == "Mask" else (0, 0, 255)

                    # inculde the probability when printing the label
                    label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)

                    # displays the label and box on the output of frame
                    cv2.putText(frame, label, (startX, startY - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
                    cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
            except:
                pass

            # show the output of frame
            cv2.imshow("Frame", frame)

            # break the loop if 'q' is pressed
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break

        self.__camera.closeVideo()
        cv2.destroyAllWindows()
    


    # Moves gripper with x and y value of joystick
    def moveGripper(self, joypos, magnet = None):
        try:
            self.__servoGripper.moveUnlimited(joypos)
            if magnet is not None:
                self.__magnet.switch(magnet)
        except: 
            print("moving gripper failed")
    

    # Moves robot with x and y value of joystick
    def move(self, speed, direction):
        try:
            self.__engine1.setValue(speed + direction)
            self.__engine2.setValue(speed - direction)
        except:
            print("moving robot failed(move)")
            self.__engine1.setValue(0)
            self.__engine2.setValue(0)

    def moveTrackControl(self, lefttrack, righttrack):
        try:
            self.__engine1.setValue(lefttrack)
            self.__engine2.setValue(righttrack)
        except:
            print("moving robot failed(trackcontrol)")
        

    # Robot dance command
    def dance(self):
        print("dance started")
        timeDelta = datetime.timedelta(minutes=100)
        timeEnd = datetime.datetime.now() + timeDelta
        while datetime.datetime.now() < timeEnd:
            low, mid, high = self.__microphone.getMaxLights()
            self.__light.setValues(low, mid, high)
        self.__light.resetLights()
        print("mic stopped")


    # returns all components
    def getComponents(self):
        return self.__camera, self.__servoGripper, self.__light, self.__engine1, self.__engine2, self.__microphone, self.__weight
