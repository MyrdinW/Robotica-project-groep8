import datetime


class Dance:
    """
    Dance makes the robot 'dance' to music
    It also lights up the lights according to the volume of different frequencies
    WIP
    """
    def __init__(self, microphone, light):
        self.__microphone = microphone
        self.__light = light

    # dance
    def run(self):
        print("dance started")
        timeDelta = datetime.timedelta(minutes=100)
        timeEnd = datetime.datetime.now() + timeDelta
        while datetime.datetime.now() < timeEnd:
            low, mid, high = self.__microphone.getMaxLights()
            self.__light.setValues(low, mid, high)
        self.__light.resetLights()
        print("mic stopped")