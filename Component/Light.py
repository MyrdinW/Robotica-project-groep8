import board
import neopixel


class Light:
    """
        Light handles all light functions ex. changing values according to incoming sounds
    """

    def __init__(self, leds):
        super().__init__()
        self.__pixelPin = board.D21
        self.__numPixels = 16
        self.__order = neopixel.RGBW
        self.__pixels = neopixel.NeoPixel(self.__pixelPin, self.__numPixels, brightness=0.2, auto_write=False,
                                          pixel_order=self.__order)

        green = [5, 4, 3, 6, 7, 8, 15, 14, 13]
        yellow = [2, 9, 12]
        red = [1, 10, 11]
        self.__colors = {}

        for i in green:
            self.__colors.update({i: (255, 0, 0, 0)})

        for i in yellow:
            self.__colors.update({i: (255, 255, 0, 0)})

        for i in red:
            self.__colors.update({i: (0, 255, 0, 0)})

        self.__leds = leds
        self.__low = 0
        self.__mid = int(self.__leds / 3)
        self.__high = int((self.__leds / 3) * 2)

        print("Light initalized")

    def setValues(self, low, mid, high):
        """
        Args:
            low: amount of lights to be enable on low frequency strip
            mid: amount of lights to be enable on mid frequency strip
            high: amount of lights to be enable on mid frequency strip
        """
        print(f"{low} {mid} {high}")
        for i in range(self.__numPixels):
            self.__pixels[i] = (0, 0, 0, 0)

        for i in range(0, 5):

            if mid >= i:
                self.__pixels[i + self.__mid] = self.__colors.get(i)

        for i in range(5, 0):
            if low >= i:
                self.__pixels[i] = self.__colors.get(i)
            if high >= i:
                self.__pixels[i + self.__high] = self.__colors.get(i)
        self.__pixels.show()

    def changeLights(self, color):
        if color == "r":
            color = (0, 255, 0, 0)
        elif color == "g":
            color = (255, 0, 0, 0)
        for i in range(len(self.__pixels)):
            self.__pixels[i] = color
        self.__pixels.show()


    def resetLights(self):
        for i in range(self.__numPixels):
            self.__pixels[i] = (0, 0, 0, 0)
        self.__pixels.show()

    def getLights(self):
        return str(self.__pixels)
