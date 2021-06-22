import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

class PowerMeter:
    def __init__(self):
        self.__spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
        self.__cs = digitalio.DigitalInOut(board.D21)
        self.__mcp = MCP.MCP3008(self.__spi, self.__cs)
        self.__channel = AnalogIn(self.__mcp, MCP.P0)

        self.__calculatedValue = 5.679862
        self.__voltage = 0

    def getValue(self):
        self.__voltage = self.__channel.voltage * self.__calculatedValue
        return self.__voltage