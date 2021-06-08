import board
import neopixel


class Light:
    """
        Light handles all light functions ex. changing values according to incoming sounds
        Board and neopixel are needed to control the Ledstrip through the RPi pins
        The Microphone class calculates the number of led's to be switched on according to the in-stream, 
        while this Light class initializes which led's should have which colours. 
        This is a repeatable process since the led's need to be be given a colour and show command, in order to turn
        led's on or off
    """

    def __init__(self, leds):
        self.__pixel_pin = board.D21
        self.__num_pixels = 16
        self.__order = neopixel.RGBW
        self.__pixels = neopixel.NeoPixel(self.__pixel_pin, self.__num_pixels, brightness=0.2, auto_write=False,
                                          pixel_order=self.__order)

        green = [0, 1, 2, 5, 6, 7, 10, 11, 12]
        yellow = [3, 8, 13]
        red = [4, 9, 14]
        self.__colors = {}

        for i in green:
            self.__colors.update({i: (255, 0, 0, 0)})

        for i in yellow:
            self.__colors.update({i: (255, 255, 0, 0)})

        for i in red:
            self.__colors.update({i: (0, 255, 0, 0)})

        self.__leds = leds
        self.__mid = int(self.__leds / 3)
        self.__high = int((self.__leds / 3) * 2)

        print("Light initialized")

    # setting the colours for each led in each frequency range.
    def set_values(self, low, mid, high):
        """
        Args:
            low: amount of lights to be enable on low frequency strip
            mid: amount of lights to be enable on mid frequency strip
            high: amount of lights to be enable on mid frequency strip
        """
        print(f"{low} {mid} {high}")
        for i in range(self.__num_pixels):
            self.__pixels[i] = (0, 0, 0, 0)

        for i in range(0, 5):
            if low >= i:
                self.__pixels[i] = self.__colors.get(i)
            if mid >= i:
                self.__pixels[i + self.__mid] = self.__colors.get(i)
            if high >= i:
                self.__pixels[i + self.__high] = self.__colors.get(i)

        self.__pixels.show()

    # resetting the lights
    def reset_lights(self):
        for i in range(self.__num_pixels):
            self.__pixels[i] = (0, 0, 0, 0)
        self.__pixels.show()

    # returns colours per led in array for telemetry website
    def get_lights(self):
        return str(self.__pixels)
