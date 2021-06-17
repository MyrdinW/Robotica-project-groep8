class LightController:

    def __init__(self, light):
        self.__light = light
        self.__mode = 0

    def speedoMeter(speedl, speedr):
        leds = 10
        startLedLeft= 63
        startLedRight = 30

        ammountLeft = int(speedl * leds)
        ammountRight = int(speedr * leds)
        output = []

        color = (255, 0, 0, 0)

        if speedl != 0:
            for i in range(startLedLeft, startLedLeft + ammountLeft):
                output.append([i, color])
        if speedr != 0:
            for i in range(startLedRight, startLedRight + ammountRight):
                output.append([i, color])
        if output != []:
            self.__light.setLights(output)
