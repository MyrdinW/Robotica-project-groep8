class Rainbow:
    def __init__(self, light):
        self.__light = light
        self.__position = 0
        self.__startIndex = 15
        self.__numPixels = 63
    
    def wheel(self, pos):
        if pos < 0 or pos > 255:
            r = g = b = 0
        elif pos < 85:
            r = int(pos * 3)
            g = int(255 - pos * 3)
            b = 0
        elif pos < 170:
            pos -= 85
            r = int(255 - pos * 3)
            g = 0
            b = int(pos * 3)
        else:
            pos -= 170
            r = 0
            g = int(pos * 3)
            b = int(255 - pos * 3)
        return (r, g, b, 0)

    def cycle(self):
        output = []
        for i in range(self.__numPixels):
            pixelIndex = (i * 256 // self.__numPixels) + self.__position
            output.append([i + self.__startIndex, self.wheel(pixelIndex & 255)])
        self.__light.setLights(output)
        self.__position += 1
        if self.__position == 256:
            self.__position = 0
