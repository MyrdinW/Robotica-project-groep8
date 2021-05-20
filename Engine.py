import RPi.GPIO as gpio

class Engine:
   
    
    def __init__(self, pin1, pin2, pin3):
        self.pwmpin = pin1
        self.fpin = pin2
        self.bpin = pin3
        gpio.setmode(gpio.BCM)
        gpio.setup(pin1, gpio.OUT)
        gpio.setup(pin2, gpio.OUT)
        gpio.setup(pin3, gpio.OUT)
        self.p = gpio.PWM(self.pwmpin, 8000)
        self.p.start(0)
        self.offset = 0
        self.value = 0
        print("motor initialized")

    def set_value(self, value):
        self.value = value
        if value == 0:
            gpio.output(self.fpin, 0)
            gpio.output(self.bpin, 0)
        if value > 0:
            gpio.output(self.fpin, 1)
            gpio.output(self.bpin, 0)
            self.p.ChangeDutyCycle(100*value)
        if value < 0:
            gpio.output(self.bpin, 1)
            gpio.output(self.fpin, 0)
            self.p.ChangeDutyCycle(100*value*-1)
        print (self.value)

    def get_value(self):
        return self.value

    def set_offset(self, offset):
        self.offset = offset

    def get_offset(self):
        return self.offset

