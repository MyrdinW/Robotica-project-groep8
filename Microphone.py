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
        print("Microphone initialized")

    def get_image(self):
        #data = np.frombuffer(self.stream.read(self.chunk), dtype=np.int16)
        #fig, axis = plt.subplots()
        #axis.plot(data, 'r')
        #axis.grid()
        #axis.set_ylim([-10000, 10000])
        #image = io.BytesIO()
        #fig.savefig(image, format="jpg")
        #image.seek(0)
        #encoded_image = base64.b64encode(image.read())
        #return encoded_image
        return ""

    def get_output(self):
        return self.output
    
    def get_maxlights(self):
        print("max lights")
        data = np.frombuffer(self.stream.read(self.chunk),dtype=np.int16)
        #data = ((data/np.power(2.0,15))*5.25)*(mic_sens_corr) 
        peak_low = 0 
        peak_mid = 0 
        peak_high = 0
        for i in range (0,200,1):
            if data[i] > data[i-1]: 
                peak_low = data[i]
        for i in range (201,2000,1):
            if data[i] > data[i-1]: 
                peak_mid = data[i]
        for i in range (2001,len(data),1):
            if data[i] > data[i-1]: 
                peak_high = data[i]    
        max_leds_low=abs(1*int(100*peak_low/2**15))
        max_leds_mid=abs(1*int(100*peak_mid/2**15)) 
        max_leds_high=abs(1*int(100*peak_high/2**15)) 
        if max_leds_low > 5:
            max_leds_low = 5
        if max_leds_mid > 5:
            max_leds_mid = 5
        if max_leds_high > 5:
            max_leds_high = 5
        return max_leds_low, max_leds_mid, max_leds_high
    
    def operation(self):
        pass
