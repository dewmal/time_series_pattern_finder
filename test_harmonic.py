import numpy as np
import pandas as pd
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt

# import our historical data
from app.pattern_utils import peak_detect
from app.patterns import is_gartley, is_butterfly, is_crab, is_bat

data = pd.read_csv("data/EURUSD_Candlestick_1_M_BID_01.09.2019-21.09.2019.csv")
data.columns = ['Date', 'open', 'high', 'low', 'close', 'vol']

data = data.drop_duplicates(keep=False)

data.Date = pd.to_datetime(data.Date, format="%d.%m.%Y %H:%M:%S.%f")

data = data.set_index(data.Date)
data = data[['open', 'high', 'low', 'close', 'vol']]

price = data.close
err_allowed = 5 / 100.0
tot_patterns = 0

for i in range(100, len(price)):

    current_idx, current_pat, start_idx, end_idx = peak_detect(price.values[:i], order=5)

    # Pattern Finding
    XA = current_pat[1] - current_pat[0]
    AB = current_pat[2] - current_pat[1]
    BC = current_pat[3] - current_pat[2]
    CD = current_pat[4] - current_pat[3]
    moves = [XA, AB, BC, CD]

    gartley = is_gartley(moves=moves, err_allowed=err_allowed)
    butterfly = is_butterfly(moves=moves, err_allowed=err_allowed)
    bat = is_bat(moves=moves, err_allowed=err_allowed)
    crab = is_crab(moves=moves, err_allowed=err_allowed)

    harmonics = np.array([gartley, butterfly, bat, crab])
    labels = ['Gartley', 'Butterfly', 'Bat', 'Crab']
    if np.any(harmonics == 1) or np.any(harmonics == -1):
        for j in range(0, len(harmonics)):
            if harmonics[j] == 1 or harmonics[j] == -1:
                sense = 'Bearish ' if harmonics[j] == -1 else 'Bullish '
                label = sense + labels[j] + ' Found'
                tot_patterns += 1
                plt.title(label)
                plt.plot(np.arange(start_idx, i + 15), price.values[start_idx:i + 15])
                plt.plot(current_idx, current_pat, c='r')
                plt.show()
