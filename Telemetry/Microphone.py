import base64
import time
import io
from Part import Part
import pyaudio
import matplotlib.pyplot as plt
import matplotlib
import numpy as np


class Microphone(Part):
    def __init__(self):
        super().__init__()
        matplotlib.use('agg')
        self.output = []
        self.rate = 44100
        self.chunk = int(self.rate / 20)
        self.audio = pyaudio.PyAudio()
        self.stream = (self.audio.open(format=pyaudio.paInt32, channels=1, rate=self.rate, input=True,
                                       frames_per_buffer=self.chunk))

    def get_image(self):
        data = np.frombuffer(self.stream.read(self.chunk, exception_on_overflow = False), dtype=np.int32)
        fig, axis = plt.subplots()
        axis.plot(data, 'r')
        axis.grid()
        axis.set_ylim([-10000, 10000])
        image = io.BytesIO()
        fig.savefig(image, format="jpg")
        image.seek(0)
        encoded_image = base64.b64encode(image.read())
        return encoded_image

    def get_output(self):
        return self.output

    def operation(self):
        pass
