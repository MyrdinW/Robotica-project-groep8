import board
import neopixel
import datetime
import time

class Light:
    """
        Light handles all light functions ex. changing values according to incoming sounds
    """

    def __init__(self, leds):
        super().__init__()
        self.__pixelPin = board.D12
        self.__numPixels = 78
        self.__order = neopixel.RGBW
        self.__pixels = neopixel.NeoPixel(self.__pixelPin, self.__numPixels, brightness=0.2, auto_write=False,
                                          pixel_order=self.__order)
        self.__lastindex = 41

        green = [2, 3, 4, 5, 6, 7, 12, 13, 14]
        yellow = [1, 8, 11]
        red = [0, 9, 10]
        self.__colors = {}

        for i in green:
            self.__colors.update({i: (255, 0, 0, 0)})

        for i in yellow:
            self.__colors.update({i: (255, 255, 0, 0)})

        for i in red:
            self.__colors.update({i: (0, 255, 0, 0)})

        self.__leds = leds - 63
        self.__low = 5
        self.__mid = int(self.__leds / 3)
        self.__high = int((self.__leds / 3) * 2)
        print("Light initalized")

    def setLights(self, array):
        for i in range(self.__numPixels):
            self.__pixels[i] = (0, 0, 0, 0)
        for pixel in array:
            self.__pixels[pixel[0]] = pixel[1]
        self.__pixels.show()
        
    def setKnightrider(self, array):
        self.__pixels[self.__lastindex] = (0,0,0,0)
        self.__pixels.show()
        for pixel in array:
            self.__pixels[pixel[0]]  = pixel[1]
            self.__lastindex = pixel[0]
        self.__pixels.show()
        time.sleep(0.05)

    def setValues(self, low, mid, high):
        """
        Args:
            low: amount of lights to be enable on low frequency strip
            mid: amount of lights to be enable on mid frequency strip
            high: amount of lights to be enable on mid frequency strip
        """
        #print(f"{low} {mid} {high}")



        for i in range(self.__numPixels):
            self.__pixels[i] = (0, 0, 0, 0)

        for i in range (4, 4 - low, -1):
            self.__pixels[i] = self.__colors.get(i)

        for i in range (5, 5 + mid):
            self.__pixels[i] = self.__colors.get(i)

        for i in range (14, 14 - high, -1):
            self.__pixels[i] = self.__colors.get(i)

        self.__pixels.show()

    def changeLights(self, color):
        #print(color)
        if color == "r":
            color = (0, 255, 0, 0)
        elif color == "g":
            color = (255, 0, 0, 0)
        else:
            color = (255, 255, 0, 0)
        for i in range(0, self.__numPixels):
            self.__pixels[i] = color
        self.__pixels.show()
        print("done")


    def resetLights(self):
        for i in range(self.__numPixels):
            self.__pixels[i] = (0, 0, 0, 0)
        self.__pixels.show()

    def getLights(self):
        return str(self.__pixels)
