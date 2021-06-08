import RPi.GPIO as gpio


class Engine:

    def __init__(self, pwmpin, fpin, bpin):
        """
        :param pwmpin:
        :param fpin:
        :param bpin:
        """
        self.__fpin = fpin
        self.__bpin = bpin
        gpio.setmode(gpio.BCM)
        gpio.setup(pwmpin, gpio.OUT)
        gpio.setup(fpin, gpio.OUT)
        gpio.setup(bpin, gpio.OUT)
        self.p = gpio.PWM(pwmpin, 8000)
        self.p.start(0)
        self.value = 0
        self.offset = 0
        print("motor initialized")

    # Changes motor value according to values from
    def setValue(self, value):
        self.value = value + self.offset
        if value == 0:
            gpio.output(self.__fpin, 0)
            gpio.output(self.__bpin, 0)

        if value > 0:
            if value > 1:
                value = 1
                
            gpio.output(self.__fpin, 1)
            gpio.output(self.__bpin, 0)
            self.p.ChangeDutyCycle(100 * value)

        if value < 0:
            if value < -1:
                value = -1
                
            gpio.output(self.__bpin, 1)
            gpio.output(self.__fpin, 0)
            self.p.ChangeDutyCycle(100 * value * -1)
        
    # returns value of engine
    def getValue(self):
        return self.value

