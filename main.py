from math import atan
from sympy import Point, Polygon
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# import our historical data
from tqdm import tqdm

from app.pattern_utils import peak_detect, get_angle
from app.patterns.flag_patterns import is_rectangle, is_pennant, is_wedge

data = pd.read_csv("data/EURUSD_Candlestick_1_M_BID_01.09.2019-21.09.2019.csv")
data.columns = ['Date', 'open', 'high', 'low', 'close', 'vol']

data = data.drop_duplicates(keep=False)

data.Date = pd.to_datetime(data.Date, format="%d.%m.%Y %H:%M:%S.%f")

data = data.set_index(data.Date)
data = data[['open', 'high', 'low', 'close', 'vol']]

price = data.close  # .iloc[:500]
order = 10
# plt.ion()

err_allowed = 5 / 100.0

for i in tqdm(range(1200, len(price))):
    values = price.values[:i]
    current_idx, current_pat, start_idx, end_idx = peak_detect(values,
                                                               order=order,
                                                               pattern_size=5)
    square_x = current_idx[-4:]
    A_x = current_idx[0]

    B_x = current_idx[1]  # np.array([current_idx[2], current_idx[1]])[np.argmin([current_pat[2], current_pat[1]])]
    C_x = current_idx[2]  # np.array([current_idx[2], current_idx[1]])[np.argmax([current_pat[2], current_pat[1]])]
    D_x = current_idx[3]  # np.array([current_idx[3], current_idx[4]])[np.argmin([current_pat[3], current_pat[4]])]
    E_x = current_idx[4]  # np.array([current_idx[3], current_idx[4]])[np.argmax([current_pat[3], current_pat[4]])]

    A_y = values[A_x]
    B_y = values[B_x]
    C_y = values[C_x]
    D_y = values[D_x]
    E_y = values[E_x]

    angle_cbd = get_angle([C_x, C_y], [B_x, B_y], [D_x, D_y]) / 360
    angle_bce = get_angle([B_x, B_y], [C_x, C_y], [E_x, E_y]) / 360
    angle_ced = get_angle([C_x, C_y], [E_x, E_y], [D_x, D_y]) / 360
    angle_edb = get_angle([E_x, E_y], [D_x, D_y], [B_x, B_y]) / 360

    angles = np.around([angle_cbd, angle_bce, angle_ced, angle_edb], decimals=2)
    # pA, pB, pC, pD, pE = None, None, None, None, None
    pA, pB, pC, pD, pE = map(Point, [(A_x, A_y), (B_x, B_y), (C_x, C_y), (D_x, D_y), (E_x, E_y)])
    pol = Polygon(pB, pC, pD, pE)
    if not pol.is_convex():
        temp_x = E_x
        E_x = D_x
        D_x = temp_x
        E_y, D_y = values[E_x], values[D_x]
        pD, pE = map(Point, [(D_x, D_y), (E_x, E_y)])
        pol = Polygon(pB, pC, pD, pE)

    BCx, BCy = [B_x, C_x], [B_y, C_y]
    CDx, CDy = [C_x, D_x], [C_y, D_y]
    DEx, DEy = [D_x, E_x], [D_y, E_y]
    EBx, EBy = [E_x, B_x], [E_y, B_y]

    # angles = [pol.angles[p].evalf() for p in [pB, pC, pD, pE]]
    # if np.all(0.5 < angles):
    # if pol.is_convex():
    # plt.clf()
    # plt.title(f"Angles B,C,E,D {angles}")
    if not pol.is_convex():
        plt.plot(np.arange(start_idx, i + 50), price.values[start_idx:i + 50])
        plt.scatter(current_idx, current_pat, c='r')
        plt.plot(BCx, BCy, c="r", linewidth=2)
        plt.plot(CDx, CDy, c="g", linewidth=2)
        plt.plot(DEx, DEy, c="b", linewidth=2)
        plt.plot(EBx, EBy, c="c", linewidth=2)
        plt.show()
    # plt.pause(0.05)
