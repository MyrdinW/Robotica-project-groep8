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
from Weight_fake import Weight_fake
from LaptopReceiver import LaptopReceiver

class Controller:
    """
        Controller handles all actions of the robot as a whole.
        It acts as a facade that handles all components
    """

    def __init__(self):
        self.__mode = 0
        #self.__sound = Sound()
        self.__engine1 = Engine(3, 4, 2)
        self.__engine2 = Engine(27, 17, 22)
        self.__servo_camera = Servo(1, 0)
        self.__servo_gripper = Servo(0, 1)
        self.__microphone = Microphone()
        self.__light = Light(15)
        self.__camera = Camera()
        self.__magnet = Magnet(25)
        
        # print("Utils starting")
        self.__utils = Utils()
        # print("Utils finished")
        self.__remote = Remote()
        self.__laptopreceiver = LaptopReceiver()
        print("test")
        # try:
        self.__weight = Weight()
        #except:
        #    print("weight failed")
        #self.__receiver = Receiver()
        #threading.Thread(target=self.listen).start()
        threading.Thread(target=self.listentolaptop).start()
        # print("controller")
        #t = threading.Thread(target=self.__sound.random_robot)
        #t.start()
        # self.mask()
        #threading.Thread(target=self.dance).start()
        #self.__engine.set_value(0.1)
        #self.mask()
        self.followline()
        
    def followstairline(self):
        for i in range(1000):
            frame = self.__camera.get_image()
            # print(frame)
            # try:
            time0 = datetime.datetime.now()
            output = self.__utils.get_distance_blue(frame, 1)
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
                self.move_track_control(0.8, 0)
                continue
            if output[0] == "right":
                print("going right")
                self.move_track_control(0, 0.8)
                continue
            self.move(0, 0)
            # except:
            #print("exception")
        self.__camera.close_video()
        cv2.destroyAllWindows()
        # exit()
        
        
    def followline(self):
        print("follow line")
        
        for i in range(1000):
            
            #time0 = datetime.datetime.now()
            frame = self.__camera.get_image()
            output = self.__utils.get_distance_blue(frame, 0)
            #print(datetime.datetime.now() - time0)
            print(output)
            
            if not output:
                self.move(0, 0)
                continue
            
            if output[1] < 50:
                self.move(0, 0)
                continue

            if output[0] == "left":
                print("going left")
                self.move(0, -0.1)
                continue
                
            elif output[0] == "right":
                print("going right")
                self.move(0, 0.1)
                continue
                    

            
            # except:
            #print("exception")
        self.__camera.close_video()
        cv2.destroyAllWindows()
        # exit()
    
    def mask(self):
        for i in range(200):
            frame = self.__camera.get_image()
            frame = imutils.resize(frame, width=800)
            try:
                locs, preds = self.__utils.detect_and_predict_mask(frame)

                for (box, pred) in zip(locs, preds):
                    (startX, startY, endX, endY) = box
                    (mask, withoutMask) = pred

                    label = "Mask" if mask > withoutMask else "No Mask"
                    if mask < withoutMask:
                        print("No mask")
                    else:
                        print("Mask")
                        # threading.Thread(target=playsound.playsound("shall.mp3")).start()

                    color = (0, 255, 0) if label == "Mask" else (0, 0, 255)

                    label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)

                    cv2.putText(frame, label, (startX, startY - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
                    cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
            except:
                pass
            cv2.imshow("Frame", frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
        self.__camera.close_video()
        cv2.destroyAllWindows()
    
    # Listens for command from the remote
    def listen(self):
        print("start listening")
        while True:
            
            command = self.__receiver.listen()
            self.__weight.get_weight()
            if command is not None:
                
                
                val = list(map(int, command))
                print(val)
                ##[int(command[0]),int(command[0]),int(command[0]),int(command[0]),int(command[0]),int(command[0])] 
                
                if val[0] == 0:
                    continue
            
                self.__remote.set_joy_positions([val[1], val[2], val[3], val[4]])
                if val[0] == 1:
                    remotepositions = self.__remote.get_move_positions()
                    print(remotepositions)
                    if remotepositions[0] is None:
                        continue
                    #self.move_track_control(remotepositions[0], remotepositions[0])
                    #self.move(remotepositions[0], remotepositions[1])
                    
                if val[0] == 2:
                    print(val[1])
                    #self.movegripper(val[1], val[2])

    def listentolaptop(self):
        print("start listening laptop")
        while True:
            command = self.__laptopreceiver.listen()
            if command is not None:
                
                
                val = list(map(int, command))
                
                print(val)
                if val[0] == 0:
                    continue
            
                self.__remote.set_joy_positions([val[1], val[2], val[3], val[4]])
                if val[0] == 1:
                    y1 = self.__remote.get_position('y1')
                    x1 = self.__remote.get_position('x1')
                    
                    #y2 = self.__remote.get_move_positions('y2')
                    if y1 is None or x1 is None:
                        continue
                    #self.move_track_control(y1, y2)
                    self.move(y1, x1)
                    
                if val[0] == 2:
                    y1 = self.__remote.get_position('y1')
                    print(y1)
                    self.movegripper(y1, val[5])

                if val[0] == 3:
                    print("test")



    # Moves gripper with x and y value of joystick
    def movegripper(self, joypos, magnet):
        self.__servo_gripper.move_unlimited(joypos)
        self.__magnet.switch(magnet)
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
        return self.__camera, self.__servo_gripper, self.__light, self.__engine1, self.__engine1, self.__microphone, self.__weight
