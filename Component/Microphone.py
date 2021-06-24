import base64
import io
import matplotlib.pyplot as plt
import wave
from struct import unpack
import numpy as np
import pyaudio


# import Robotconfig


class Microphone:
    """
    Microphone handles all actions with the microphone
    """

    def __init__(self):
        super().__init__()
        self.__data = None
        self.__rate = 44100
        self.__chunk = 4096
        self.__audio = pyaudio.PyAudio()
        self.__stream = (self.__audio.open(format=pyaudio.paInt16, channels=1, rate=self.__rate, input=True,
                                           frames_per_buffer=self.__chunk))
        print("Microphone initialized")

        self.__matrix = [0, 0, 0]
        self.__power = []
        self.__weighting = [8,16,32]

    def piff(self, val):
        return int(2 * self.__chunk * val / self.__rate)

    def calculate_levels(self, data, chunk, rate):
        global matrix
        # Convert raw data (ASCII string) to numpy array
        data = unpack("%dh" % (len(data) / 2), data)
        data = np.array(data, dtype='h')
        # Apply FFT - real data
        fourier = np.fft.rfft(data)
        # Remove last element in array to make it the same size as chunk
        fourier = np.delete(fourier, len(fourier) - 1)
        # Find average 'amplitude' for specific frequency ranges in Hz
        power = np.abs(fourier)
        self.__matrix[0] = int(np.mean(power[self.piff(0):self.piff(200):1]))
        self.__matrix[1] = int(np.mean(power[self.piff(200):self.piff(2000):1]))
        self.__matrix[2] = int(np.mean(power[self.piff(2000):self.piff(20000):1]))

        # Tidy up column values for the LED matrix
        self.__matrix = np.divide(np.multiply(self.__matrix, self.__weighting), 1000000)
        # Set floor at 0 and ceiling at 8 for LED matrix
        self.__matrix = self.__matrix.clip(0, 5)
        return self.__matrix

    def update(self):
        while True:
            self.__data = self.__stream.read(self.__chunk)
            matrix = self.calculate_levels(self.__data, self.__chunk, self.__rate)
            self.__nlows = int(matrix[0] * 1.6)
            self.__nmids = int(matrix[1] * 3)
            self.__nhighs = int(matrix[2] * 10)
            if(self.__nlows) > 5:
                self.__nlows = 5
            if(self.__nmids) > 5:
                self.__nmids = 5
            if(self.__nhighs) > 5:
                self.__nhighs = 5

    # Gets amounts of lights to be on for each frequency range
    def getMaxLights(self):
        return self.__nlows, self.__nmids, self.__nhighs


