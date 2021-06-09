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
        measures = self.__hx711.get_raw_data()
        measures = np.asarray(measures)
        results = []
        
        for measure in measures:
            results.append((measure + 1228161) / 556)
        #print(results)
        print(str(np.average(results)) + "g")
        return str(np.average(results)) + "g"
