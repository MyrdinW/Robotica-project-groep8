from hx711 import HX711
import numpy as np


class Weight:
    def __init__(self):
        self.hx711 = HX711(dout_pin=22, pd_sck_pin=27, channel="A", gain=64)
        self.hx711.reset()

    def get_weight(self):
        measures = self.hx711.get_raw_data()
        measures = np.asarray(measures)
        results = []
        for measure in measures:
            results.append((measure + 98889) / -548)
        print(np.average(results) + "g")
        return np.average(results)
