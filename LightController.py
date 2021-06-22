from ledeffects.Knightrider import Knightrider
from ledeffects.Rainbow import Rainbow

import datetime
import time

class LightController:

    def __init__(self, light):
        self.__light = light
        self.__mode = 0

        #colors
        self.__colorGreen = (255, 0, 0, 0)
        self.__colorRed = (0, 255, 0, 0)
        self.__colorBlue = (0, 0, 255, 0)
        self.__colorWhite = (0, 0, 0, 255)

        #data for speedometer
        self.__ledsSpeedoMeter = 10
        self.__startLedSpeedoMeterLeft= 63
        self.__startLedSpeedoMeterRight = 30

        self.rainbow = Rainbow(light)
        self.knightrider = Knightrider(light)

        

    def speedoMeter(self, speedl, speedr):

        amountLeft = int(speedl * self.__ledsSpeedoMeter)
        amountRight = int(speedr * self.__ledsSpeedoMeter)
        output = []

        for i in range(41, 44):
            output.append([i, self.__colorWhite])

        for i in range(50, 53):
            output.append([i, self.__colorWhite])

        for i in range(16, 19):
            output.append([i, self.__colorBlue])

        for i in range(75, 78):
            output.append([i, self.__colorBlue])

        if speedl > 0:
            for i in range(self.__startLedSpeedoMeterLeft, self.__startLedSpeedoMeterLeft - amountLeft, -1):
                output.append([i, self.__colorGreen])
        elif speedl < 0:
            for i in range(self.__startLedSpeedoMeterLeft, self.__startLedSpeedoMeterLeft - amountLeft):
                output.append([i, self.__colorRed])
        if speedr > 0:
            for i in range(self.__startLedSpeedoMeterRight, self.__startLedSpeedoMeterRight + amountRight):
                output.append([i, self.__colorGreen])
        elif speedr < 0:
            for i in range(self.__startLedSpeedoMeterRight, self.__startLedSpeedoMeterRight + amountRight, -1):
                output.append([i, self.__colorRed])

        self.__light.setLights(output)

    


    

        


            
            
