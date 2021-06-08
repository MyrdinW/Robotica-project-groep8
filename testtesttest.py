import numpy as np
from hx711 import HX711


class Weight:
    """
    Weight handles component to weigh objects with a margin of 5g
    """
    def __init__(self):
        self.__hx711 = HX711(dout_pin=13, pd_sck_pin=19, channel="A", gain=64)
        self.__hx711.reset()
        print("Weight init")

    def getWeight(self):
        value = 0
        for i in range(20):
            measures = self.__hx711.get_raw_data()
            measures = np.asarray(measures)
            measures = [measure for measure in measures if measure >= -1230000 and measure <= -1225000]
            results = []
            print(measures)
            #for measure in measures:
            #    results.append((measure / 547)+2246)
            #print(results)
            #print(str(np.average(results)) + "g")
            value += np.average(measures)
            # return str(np.average(results)) + "g"
            print(np.average(measures))
        print(value / 20)

