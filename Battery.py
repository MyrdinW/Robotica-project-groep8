import busio
import digitalio
import board
import time
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

class Battery:
    def __init__(self):
        self.spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
        self.cs = digitalio.DigitalInOut(board.D21)
        self.mcp = MCP.MCP3008(self.spi, self.cs)
        self.channel = AnalogIn(self.mcp, MCP.P0)
    
    def get_voltage(self):
        # print(self.channel.voltage *5.679862)
        time.sleep(1)
        return self.channel.voltage *5.679862

battery = Battery()
print(battery.get_voltage())