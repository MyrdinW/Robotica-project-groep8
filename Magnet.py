import RPi.GPIO as GPIO

class Magnet:
    def __init__(self, pin):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT) 
        self.__pin = pin
        self.__value = 0
        
    def switch(self, value):
        if value != self.__value:
            GPIO.output(self.__pin, value)
            self.__value = value
        
    def getvalue(self):
        return self.__value
        