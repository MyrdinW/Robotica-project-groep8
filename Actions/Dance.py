class Dance:
    def __init__(self, microphone, light):
        self.__microphone = microphone
        self.__light = light

    def run(self):
        print("dance started")
        timeDelta = datetime.timedelta(minutes=100)
        timeEnd = datetime.datetime.now() + timeDelta
        while datetime.datetime.now() < timeEnd:
            low, mid, high = self.__microphone.getMaxLights()
            self.__light.setValues(low, mid, high)
        self.__light.resetLights()
        print("mic stopped")