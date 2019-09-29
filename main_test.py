import timeit
import traceback

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pyti.simple_moving_average import simple_moving_average
from pyti.exponential_moving_average import exponential_moving_average

from app.patterns.moving_avg_patterns import moving_average_signal

# import our historical data

data = pd.read_csv("data/EURUSD_Candlestick_1_M_BID_01.09.2019-21.09.2019.csv")
data.columns = ['Date', 'open', 'high', 'low', 'close', 'vol']

data = data.drop_duplicates(keep=False)

data.Date = pd.to_datetime(data.Date, format="%d.%m.%Y %H:%M:%S.%f")

data = data.set_index(data.Date)
data = data[['open', 'high', 'low', 'close', 'vol']]
price = data.close
order = 10
pattern_size = 10
plt.ion()
number_of_twisted_points = 3
from_last_twisted_point_to_forward = 3
direction_error = 10 / 100
consecutive_error = 15 / 100
twisted_point_diff = 0.5 / 100
for idx in range(100, len(price)):
    start = timeit.default_timer()
    try:
        values = price.values[idx - 100:idx]
        feature_values = price.values[idx - 100:idx + 20]
        sma_one = simple_moving_average(values, 14)
        sma_two = exponential_moving_average(values, 21)

        max_cut_point = 21

        values, feature_values, sma_one, sma_two = values[max_cut_point:], feature_values[max_cut_point:], sma_one[
                                                                                                           max_cut_point:], sma_two[
                                                                                                                            max_cut_point:]

        pattern, x_point = moving_avg_direction = moving_average_signal(values, sma_one, sma_two,
                                                                        consecutive_error=consecutive_error,
                                                                        direction_error=direction_error)

        title = ""
        if pattern is not np.nan:
            title = "Bullish " if pattern == 1 else "Bearish"

            stop = timeit.default_timer()
            print('Time: ', stop - start)
            plt.clf()
            plt.title(title)
            plt.plot(feature_values, c="r")
            plt.axvline(x_point, c="g")
            plt.plot(sma_one, c="c", label='SMA 14')
            plt.plot(sma_two, c="g", label='SMA 21')
            plt.legend()
            plt.show()
            plt.pause(0.75)
        #
    except Exception as e:
        print(e)
        e.with_traceback(traceback)
        traceback.print_tb(e.__traceback__)
    finally:
        stop = timeit.default_timer()
