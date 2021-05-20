from Part import Part
import neopixel
import board

class Light(Part):
    def __init__(self):
        super().__init__()
        print("Light initalized")
        self.pixel_pin = board.D21
        self.num_pixels = 16
        self.ORDER = neopixel.RGBW
        self.pixels = neopixel.NeoPixel(self.pixel_pin, self.num_pixels, brightness=0.2, auto_write=False, pixel_order=self.ORDER)

    def set_values(self, low, mid, high):
        for i in range(self.num_pixels):
            self.pixels[i] = (0, 0, 0, 0)

        c_low = 0
        c_mid = 0
        c_high = 0
        
        while c_low <= low:
            #print("%s"%(max_leds))

            if c_low <= 2:
                self.pixels[c_low] = (255, 0, 0, 0) #green
            elif c_low == 3:
                self.pixels[c_low] = (255, 255, 0, 0) #yellow
            else:
                self.pixels[c_low] = (0, 255, 0, 0) #red
            c_low+=1

        while c_mid <= mid:
            #print("%s"%(max_leds))

            if c_mid <= 2:
                self.pixels[c_mid + 5] = (255, 0, 0, 0) #green
            elif c_mid == 3:
                self.pixels[c_mid + 5] = (255, 255, 0, 0) #yellow
            else:
                self.pixels[c_mid + 5] = (0, 255, 0, 0) #red
            c_mid+=1

        while c_high <= high:
            #print("%s"%(max_leds))

            if c_high <= 2:
                self.pixels[c_high + 10] = (255, 0, 0, 0) #green
            elif c_high == 3:
                self.pixels[c_high + 10] = (255, 255, 0, 0) #yellow
            else:
                self.pixels[c_high + 10] = (0, 255, 0, 0) #red
            c_high+=1

        self.pixels.show() #show leds
    def reset_lights(self):  
        for i in range(self.num_pixels):
            self.pixels[i] = (0, 0, 0, 0)
        self.pixels.show() #show leds
    def get_value(self):
        return ""
        # return self.value
