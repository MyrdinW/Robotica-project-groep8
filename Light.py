import board
import neopixel


class Light:
    """
        Light handles all light functions ex. changing values according to incoming sounds
    """

    def __init__(self):
        super().__init__()
        self.__pixel_pin = board.D21
        self.__num_pixels = 16
        self.__order = neopixel.RGBW
        self.__pixels = neopixel.NeoPixel(self.__pixel_pin, self.__num_pixels, brightness=0.2, auto_write=False,
                                          pixel_order=self.__order)
        self.__colors = {}
        for i in range(16):
            if i <= 2:
                self.__colors.update({i: (255, 0, 0, 0)})
            elif i == 3:
                self.__colors.update({i: (255, 255, 0, 0)})
            else:
                self.__colors.update({i: (0, 255, 0, 0)})

        print("Light initalized")

    def set_values(self, low, mid, high):
        """
        Args:
            low: amount of lights to be enable on low frequency strip
            mid: amount of lights to be enable on mid frequency strip
            high: amount of lights to be enable on mid frequency strip
        """
        for i in range(self.__num_pixels):
            self.__pixels[i] = (0, 0, 0, 0)

        for i in range(0, low + 1):
            self.__pixels[low] = self.__colors.get(low)

        for i in range(0, mid + 1):
            self.__pixels[mid] = self.__colors.get(mid)

        for i in range(0, high + 1):
            self.__pixels[high] = self.__colors.get(high)
        self.__pixels.show()

    def reset_lights(self):
        for i in range(self.__num_pixels):
            self.__pixels[i] = (0, 0, 0, 0)
        self.__pixels.show()

    def get_lights(self):
        return str(self.__pixels)
