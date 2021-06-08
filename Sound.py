import playsound
import os
import random


class Sound:
    """
    Sound handles all sound coming from the robot, it uses the playsound library to play sounds
    """
    def __init__(self):
        self.__r2d2 = os.listdir("sounds/r2d2")
        self.__relevant = os.listdir("sounds/makes_sense")
        self.__nsfw = os.listdir("sounds/nsfs")

    # random robot sound
    def randomRobot(self):
        playsound.playsound(f"sounds/rd2d/{random.choice(self.__r2d2)}")
        # os.system(f"mpg321 sounds/r2d2/integratie.mp3")

    # random funny sound
    def randomRelevant(self):
        playsound.playsound(f"sounds/makes_sense/{random.choice(self.__relevant)}")

    # random nsfs sound
    def randomNsfs(self):
        playsound.playsound(f"sounds/nsfs/{random.choice(self.__nsfw)}")
