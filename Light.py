import board
import neopixel


class Light:
    """
        Light handles all light functions ex. changing values according to incoming sounds
    """

    def __init__(self, leds):
        super().__init__()
        self.__pixel_pin = board.D21
        self.__num_pixels = 16
        self.__order = neopixel.RGBW
        self.__pixels = neopixel.NeoPixel(self.__pixel_pin, self.__num_pixels, brightness=0.2, auto_write=False,
                                          pixel_order=self.__order)
        
        low = [0,1,2,5,6,7,10,11,12]
        mid= [3,8,13]
        high =[4,9,14]
        self.__colors = {}
        
        for i in low:
            self.__colors.update({i: (255, 0, 0, 0)})
            
        for i in mid:
           self.__colors.update({i: (255, 255, 0, 0)})
        
        for i in high:
            self.__colors.update({i: (0, 255, 0, 0)})

        self.__leds = leds   
        self.__low = 0
        self.__mid = int(self.__leds / 3)
        self.__high = int((self.__leds / 3) * 2)
        

        print("Light initalized")

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
        # time.sleep(1)

    def reset_lights(self):
        for i in range(self.__num_pixels):
            self.__pixels[i] = (0, 0, 0, 0)
        self.__pixels.show()

    def get_lights(self):
        return str(self.__pixels)
