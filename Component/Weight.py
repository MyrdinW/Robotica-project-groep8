import numpy as np
import time
from hx711 import HX711


class Weight:
    """
    Weight handles component to weigh objects with a margin of 5g
    """
    def __init__(self):
        self.__hx711 = HX711(dout_pin=13, pd_sck_pin=19, channel="A", gain=64)
        # self.__hx711.set_reading_format("MSB", "MSB")
        self.__hx711.reset()
        self.__weight = 0
        print("Weight init")

    def update(self):
        
        while True:
            print("update weight")
            resultsFinal = []
            results = []
            ranges = []

            for i in range(5):
                measures = self.__hx711.get_raw_data()
                measures = np.asarray(measures)
                for measure in measures:
                    result = (measure + 1231210) / 559.5
                    results.append(result)
                    ranges.append(int(result / 50) + 1000)

            commonRange = np.bincount(ranges).argmax() - 1000
            bottom = commonRange * 50 - 100
            top = commonRange * 50 + 150



            #average = np.average(results)
            #bottom = average - 500
            #top = average + 500
            #print(bottom)
            #print(top)
            for result in results:
                if bottom < result and result < top:

                    resultsFinal.append(result)
            #resultsFinal = [result for result in results if average * 0.8 < result < average * 1.2]
            # print(str(np.average(resultsFinal)) + "g")
            self.__weight =  str(np.average(resultsFinal)) + "g"
            print(self.__weight)

    def getWeight(self):
        return self.__weight

