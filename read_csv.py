import pandas as pd
import numpy as np

class CSV:

    def __init__(self, dir, file_path) -> None:
        self.dir = dir
        self.file_path = file_path

    def __str__(self) -> str:
        return "Dir: %s\nFile Path: %s" % (self.dir, self.file_path)

    # Used to get the feature
    def read_file_for(self, feature, side):
        if (feature == "stride_length"):
            return self.generate_stride_length(side)

        df = pd.read_csv(self.file_path)

        res = df[feature].tolist()

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
            "key": side
        }

        return crit

    def generate_list(self, feature):
        df = pd.read_csv(self.file_path)

        res = df[feature].tolist()
        res.sort()

        return res

    # Used to calculate the stride length using the special formula
    def generate_stride_length(self, side):
        df = pd.read_csv(self.file_path)

        a = df["stride_pace"].tolist()
        b = df["step_rate"].tolist()

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
            "key": side
        }

        return crit