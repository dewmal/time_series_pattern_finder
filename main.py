import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# import our historical data
from app.pattern_utils import peak_detect
from app.patterns.flag_patterns import is_rectangle, is_pennant, is_wedge

data = pd.read_csv("data/EURUSD_Candlestick_1_M_BID_01.09.2019-21.09.2019.csv")
data.columns = ['Date', 'open', 'high', 'low', 'close', 'vol']

data = data.drop_duplicates(keep=False)

data.Date = pd.to_datetime(data.Date, format="%d.%m.%Y %H:%M:%S.%f")

data = data.set_index(data.Date)
data = data[['open', 'high', 'low', 'close', 'vol']]

price = data.close  # .iloc[:500]
order = 10
plt.ion()
error_allowed = 0.00035 / 100
for i in range(1200, len(price)):
    values = price.values[:i]
    current_idx, current_pat, start_idx, end_idx = peak_detect(values,
                                                               order=order,
                                                               pattern_size=5)
    # print(max(current_idx[3], current_idx[4]))
    # print(min(current_idx[3], current_idx[4]))
    # print(current_idx)
    square_x = current_idx[-4:]
    A_x = current_idx[0]

    # square_x = square_x[np.argsort(current_pat[-4:])]
    # print(square_x)

    C_x = np.array([current_idx[2], current_idx[1]])[np.argmax([current_pat[2], current_pat[1]])]
    B_x = np.array([current_idx[2], current_idx[1]])[np.argmin([current_pat[2], current_pat[1]])]
    E_x = np.array([current_idx[3], current_idx[4]])[np.argmax([current_pat[3], current_pat[4]])]
    D_x = np.array([current_idx[3], current_idx[4]])[np.argmin([current_pat[3], current_pat[4]])]

    A_y = values[A_x]
    B_y = values[B_x]
    C_y = values[C_x]
    D_y = values[D_x]
    E_y = values[E_x]

    x_pos = [A_x, B_x, C_x, D_x, E_x]
    y_pos = [A_y, B_y, C_y, D_y, E_y]

    rectangle = is_rectangle(x_pos, y_pos, error_allowed)
    pennant = is_pennant(x_pos, y_pos, error_allowed)
    wedge = is_wedge(x_pos, y_pos, error_allowed)

    flags = np.array([0, 0, wedge])
    labels = ['Rectangle', 'Pennant', 'Wedge']

    BC_x = [A_x, C_x]
    CE_x = [C_x, E_x]
    BD_x = [B_x, D_x]

    AC_y = values[AC_x]
    CE_y = values[CE_x]
    BD_y = values[BD_x]

    if np.any(flags == 1) or np.any(flags == -1):
        for j in range(0, len(flags)):
            if flags[j] == 1 or flags[j] == -1:
                sense = 'Bearish ' if flags[j] == -1 else 'Bullish '
                label = sense + labels[j] + ' Found'
                plt.clf()
                plt.title(label)
                plt.plot(np.arange(start_idx, i + 50), price.values[start_idx:i + 50])
                plt.scatter(current_idx, current_pat, c='r')
                plt.plot(CE_x, CE_y, c="r", linewidth=2)
                plt.plot(BD_x, BD_y, c="g", linewidth=2)
                plt.show()
                plt.pause(0.05)
