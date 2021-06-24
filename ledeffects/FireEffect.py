import random

class FireEffect:

    def __init__(self, light):
        self.__light = light
        self.__leds = 25
        self.__cooling = 20
        self.__heat = [0] * self.__leds
        self.__sparking = 120
        

    def cycle(self):
        self.__output = []
        for i in range(0, (self.__leds - 1)):
            cooldown = random.randint(0, int(((self.__cooling * 10) / self.__leds) + 2))
            if cooldown > self.__heat[i]:
                self.__heat[i] = 0
            else:
                self.__heat[i] = self.__heat[i] - cooldown
            
        for i in range((self.__leds - 1), 2, -1):
            self.__heat[i] = (self.__heat[i - 1] + self.__heat[i - 2] + self.__heat[i-2]) / 3

        #self.__heat[3] = 255
        #self.__heat[4] = 255
        #self.__heat[5] = 255
        #if random.randint(0, 255) < self.__sparking:
        #    x = random.randint(0, 7)
        #    self.__heat[x] = self.__heat[x] + random.randint(160, 255)

        for i in range(0, self.__leds - 1):
            self.setOutput(i, self.__heat[i])

        self.__light.setLights(self.__output)


    def setOutput(self, led, temperature):
        value = int((temperature/255)*191)
        heatramp = bytes(value)
        heatramp = value & 0x3F
        heatramp <<= 2

        if value > 160:
            self.__output.append([47 + led, (255, 255, int(heatramp), 0)])
            self.__output.append([46 - led, (255, 255, int(heatramp), 0)])
        elif value > 40:
            self.__output.append([47 + led, (int(heatramp), 255, 0, 0)])
            self.__output.append([46 - led, (int(heatramp), 255, 0, 0)])
        else:
            self.__output.append([47 + led, (0, int(heatramp), 0, 0)])
            self.__output.append([46 - led, (0, int(heatramp), 0, 0)])
    
    def spark(self):
        self.__heat[0] = 255
        self.__heat[1] = 255




    