import numpy as np
import pandas as pd
from scipy.signal import argrelextrema


def peak_detect(price, order):
    # Find relative extrema
    max_idx = list(argrelextrema(price, np.greater, order=order)[0])
    min_idx = list(argrelextrema(price, np.less, order=order)[0])
    # Concat extrema
    idx = max_idx + min_idx + [len(price) - 1]
    idx.sort()

    current_idx = idx[-5:]

    start_idx = min(current_idx)
    end_idx = max(current_idx)

    current_pat = price[current_idx]

    return current_idx, current_pat, start_idx, end_idx
