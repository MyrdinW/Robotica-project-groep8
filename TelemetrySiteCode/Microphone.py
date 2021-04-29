import base64
import time
import io
from Part import Part
import pyaudio
import pylab as plt
import numpy as np


class Microphone(Part):
    def __init__(self):
        super().__init__()
        self.output = []
        self.rate = 44100
        self.chunk = int(self.rate / 20)
        self.audio = pyaudio.PyAudio()
        self.stream = (self.audio.open(format=pyaudio.paInt16, channels=1, rate=self.rate, input=True,
                                       frames_per_buffer=self.chunk))

    def get_image(self):
        t1 = time.time()
        data = np.frombuffer(self.stream.read(self.chunk), dtype=np.int16)
        fig, ax = plt.subplots()
        ax.plot(data, 'r')
        # plt.title(i)
        ax.grid()
        ax.axis([0, len(data), 0, 2 ** 16 / 2])
        image = io.BytesIO()
        fig.savefig(image, format="jpg")
        image.seek(0)
        encoded_image = base64.b64encode(image.read())
        return encoded_image

    def get_output(self):
        return self.output

    def operation(self):
        pass
