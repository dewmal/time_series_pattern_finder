import math

import numpy as np
import pandas as pd
from scipy.signal import argrelextrema


def get_angle(a, b, c):
    ang = math.degrees(math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0]))
    return ang + 360 if ang < 0 else ang


def peak_detect(price, order, pattern_size=5):
    # Find relative extrema
    max_idx = list(argrelextrema(price, np.greater, order=order)[0])
    min_idx = list(argrelextrema(price, np.less, order=order)[0])
    # Concat extrema
    idx = max_idx + min_idx + [len(price) - 1]
    idx.sort()

    current_idx = idx[-pattern_size:]

    start_idx = min(current_idx)
    end_idx = max(current_idx)

    current_pat = price[current_idx]

    return current_idx, current_pat, start_idx, end_idx


def line(p1, p2):
    A = (p1[1] - p2[1])
    B = (p2[0] - p1[0])
    C = (p1[0] * p2[1] - p2[0] * p1[1])
    return A, B, -C


def intersection(L1, L2):
    D = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    if D != 0:
        x = Dx / D
        y = Dy / D
        return x, y
    else:
        return False
