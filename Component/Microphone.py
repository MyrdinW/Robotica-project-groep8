import base64
import io
import matplotlib.pyplot as plt
import numpy as np
import pyaudio
#import Robotconfig 


class Microphone:
    """
    Microphone handles all actions with the microphone
    """

    def __init__(self):
        super().__init__()
        self.__rate = 44100
        self.__chunk = int(self.__rate / 20)
        self.__audio = pyaudio.PyAudio()
        self.__stream = (self.__audio.open(format=pyaudio.paInt16, channels=1, rate=self.__rate, input=True,
                                           frames_per_buffer=self.__chunk))
        print("Microphone initialized")

    # returns encoded image of sound waves
    def getImage(self):
        data = np.frombuffer(self.__stream.read(self.__chunk), dtype=np.int16)
        fig, axis = plt.subplots()
        axis.plot(data, 'r')
        axis.grid()
        axis.set_ylim([-10000, 10000])
        image = io.BytesIO()
        fig.savefig(image, format="jpg")
        image.seek(0)
        encodedImage = base64.b64encode(image.read())
        return encoded_image

    # Gets amounts of lights to be on for each frequency range
    def getMaxLights(self):
        data = np.frombuffer(self.__stream.read(self.__chunk), dtype=np.int16)
        peakLow = max(data[:200])
        peakMid = max(data[200:2000])
        peakHigh = max(data[2000:])

        ledsLow = self.getAmount(peakLow)
        ledsMid = self.getAmount(peakMid)
        ledsHigh = self.getAmount(peakHigh)
        return ledsLow, ledsMid, ledsHigh

    # return amount of lights according to peak of  each frequency range
    def getAmount(self, peak):
        lights = abs(1 * int(100 * peak / 2 ** 15))
        if lights > 5:
            return 5
        return lights
