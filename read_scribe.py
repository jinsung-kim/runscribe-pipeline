# import pandas as pd
import numpy as np

class ScribeData:

    def __init__(self, dir, data, id) -> None:
        '''
        dif ->  "left" or "right"
        data -> A dictionary of data for each value
        id ->   ID of the session
        '''

        self.dir = dir
        self.data = data
        self.id = id

    # Used to get the feature
    def read_file_for(self, feature):
        if (feature == "stride_length"):
            return self.generate_stride_length()

        res = self.data[self.dir][feature]

        res.sort() # Sorts in ascending order

        q1 = np.quantile(res, 0.25)
        q3 = np.quantile(res, 0.75)
        interQuantileRange = q3 - q1
        mi = q1 - 1.5 * interQuantileRange
        ma = q1 + 1.5 * interQuantileRange
        med = np.quantile(res, 0.5)

        crit = {
            "q1": q1,
            "median": med,
            "q3": q3,
            "interQuantileRange": q3 - q1,
            "min": mi,
            "max": ma,
            "key": self.dir
        }

        return crit

    # Used to calculate the stride length using the special formula
    def generate_stride_length(self):
        res = self.data

        a = res[self.dir]["stride_pace"]
        b = res[self.dir]["step_rate"]

        res = []

        # Formula for stride length
        # res = (a * 60 * 2) / b

        for i in range(len(a)):
            res.append((a[i] * 60 * 2) / b[i])

        res.sort()

        q1 = np.quantile(res, 0.25)
        q3 = np.quantile(res, 0.75)
        interQuantileRange = q3 - q1
        mi = q1 - 1.5 * interQuantileRange
        ma = q1 + 1.5 * interQuantileRange
        med = np.quantile(res, 0.5)

        crit = {
            "q1": q1,
            "median": med,
            "q3": q3,
            "interQuantileRange": q3 - q1,
            "min": mi,
            "max": ma,
            "key": self.dir
        }

        return crit