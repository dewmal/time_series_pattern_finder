import numpy as np
import pandas as pd
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt

# import our historical data
from app.pattern_utils import peak_detect

data = pd.read_csv("data/EURUSD_Candlestick_1_M_BID_01.09.2019-21.09.2019.csv")
data.columns = ['Date', 'open', 'high', 'low', 'close', 'vol']

data = data.drop_duplicates(keep=False)

data.Date = pd.to_datetime(data.Date, format="%d.%m.%Y %H:%M:%S.%f")

data = data.set_index(data.Date)
data = data[['open', 'high', 'low', 'close', 'vol']]

price = data.close
err_allowed = 10 / 100.0
for i in range(100, len(price)):

    idx, current_pat, start_idx, end_idx = peak_detect(price.values[:i], order = 10)

    # Pattern Finding
    XA = current_pat[1] - current_pat[0]
    AB = current_pat[2] - current_pat[1]
    BC = current_pat[3] - current_pat[2]
    CD = current_pat[4] - current_pat[3]

    if XA > 0 and AB < 0 and BC > 0 and CD < 0:
        # print("pat")
        # Range
        AB_range = np.array([0.618 - err_allowed, 0.618 + err_allowed]) * abs(XA)
        BC_range = np.array([0.382 - err_allowed, 0.886 + err_allowed]) * abs(AB)
        CD_range = np.array([1.27 - err_allowed, 1.618 + err_allowed]) * abs(BC)

        # print(AB_range, abs(AB))
        if AB_range[0] < abs(AB) < AB_range[1] and BC_range[0] < abs(BC) < BC_range[1] and CD_range[0] < abs(CD) < \
                CD_range[1]:
            plt.plot(np.arange(start_idx, i + 15), price.values[start_idx:i + 15])
            plt.plot(current_idx, current_pat, c='r')
            plt.show()
    elif XA < 0 and AB > 0 and BC < 0 and CD > 0:
        # print("pat")
        # Range
        AB_range = np.array([0.618 - err_allowed, 0.618 + err_allowed]) * abs(XA)
        BC_range = np.array([0.382 - err_allowed, 0.886 + err_allowed]) * abs(AB)
        CD_range = np.array([1.27 - err_allowed, 1.618 + err_allowed]) * abs(BC)

        # print(AB_range, abs(AB))
        if AB_range[0] < abs(AB) < AB_range[1] and BC_range[0] < abs(BC) < BC_range[1] and CD_range[0] < abs(CD) < \
                CD_range[1]:
            plt.plot(np.arange(start_idx, i + 15), price.values[start_idx:i + 15])
            plt.plot(current_idx, current_pat, c='r')
            plt.show()
