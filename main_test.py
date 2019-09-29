import timeit
import traceback

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from ax import optimize
from pyti.simple_moving_average import simple_moving_average
from pyti.exponential_moving_average import exponential_moving_average
from tqdm import tqdm

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
direction_error = 5 / 100
consecutive_error = 10 / 100
twisted_point_diff = 0.5 / 100
ema_fast_v, ema_slow_v = 14, 21
prediction_index = 30


def evaluate_moving_avg(number_of_twisted_points=3,
                        from_last_twisted_point_to_forward=3,
                        direction_error=5 / 100,
                        consecutive_error=10 / 100,
                        ema_fast_v=14, ema_slow_v=21,
                        prediction_index=30):
    print("--start--")
    print(number_of_twisted_points,
          from_last_twisted_point_to_forward,
          direction_error,
          consecutive_error,
          ema_fast_v, ema_slow_v,
          prediction_index)

    corrections = []
    for idx in tqdm(range(100, len(price) - prediction_index)):
        try:
            values = price.values[idx - 100:idx]
            feature_values = price.values[idx - 100:idx + prediction_index]
            prediction_values = price.values[idx:idx + prediction_index]
            ema_fast = simple_moving_average(values, ema_fast_v)
            sma_slow = simple_moving_average(values, ema_slow_v)

            max_cut_point = max([ema_slow_v, ema_fast_v])

            values, feature_values, ema_fast, sma_slow = values[max_cut_point:], feature_values[
                                                                                 max_cut_point:], ema_fast[
                                                                                                  max_cut_point:], sma_slow[
                                                                                                                   max_cut_point:]

            pattern, x_point = moving_average_signal(values, ema_fast, sma_slow,
                                                     number_of_twisted_points=number_of_twisted_points,
                                                     from_last_twisted_point_to_forward=from_last_twisted_point_to_forward,
                                                     consecutive_error=consecutive_error,
                                                     direction_error=direction_error)

            if pattern is not np.nan:
                true_value = prediction_values[0] - prediction_values[-1]
                real_trend = 0
                if true_value > 0:
                    real_trend = -1
                else:
                    real_trend = 1
                corrections.append(real_trend == pattern)
            #
        except Exception as e:
            print(e)
            e.with_traceback(traceback)
            traceback.print_tb(e.__traceback__)
        finally:
            pass
    corrections = np.array(corrections)
    correction_val = len(np.where(corrections)[0]) * 100 / len(corrections)
    prediction_rate = len(corrections) * 100 / idx
    print(f"Correction {len(corrections)},{idx} {prediction_rate} {correction_val}")
    print(f"Rate {(correction_val + prediction_rate) / 2}")
    return (correction_val + prediction_rate) / 2


if True:
    v = {'number_of_twisted_points': 2, 'from_last_twisted_point_to_forward': 2,
         'consecutive_error': 0.052611910402774804, 'ema_fast_v': 14, 'ema_slow_v': 32, 'prediction_index': 6,
         'direction_error': 0.1}

    evaluate_moving_avg(
        number_of_twisted_points=int(v["number_of_twisted_points"]),
        from_last_twisted_point_to_forward=int(v["from_last_twisted_point_to_forward"]),
        direction_error=float(v["direction_error"]),
        consecutive_error=float(v["consecutive_error"]),
        ema_fast_v=int(v["ema_fast_v"]), ema_slow_v=int(v["ema_slow_v"]),
        prediction_index=int(v["prediction_index"]),
    )

# number_of_twisted_points = 3,
# from_last_twisted_point_to_forward = 3,
# direction_error = 5 / 100,
# consecutive_error = 10 / 100,
# twisted_point_diff = 0.5 / 100,
# ema_fast_v = 14, ema_slow_v = 21,
# prediction_index = 30
if False:
    best_parameters, best_values, experiment, model = optimize(
        parameters=[
            {
                "name": "number_of_twisted_points",
                "type": "range",
                "value_type": "int",
                "bounds": [2, 6],
            },
            {
                "name": "from_last_twisted_point_to_forward",
                "type": "range",
                "value_type": "int",
                "bounds": [2, 5],
            },
            {
                "name": "direction_error",
                "type": "fixed",
                "value_type": "float",
                "value": 10 / 100
            },
            {
                "name": "consecutive_error",
                "type": "range",
                "value_type": "float",
                "bounds": [0.5 / 100, 25 / 100],
            },
            {
                "name": "ema_fast_v",
                "type": "choice",
                "value_type": "int",
                "values": [9, 14, 12, 15, 17],
            }, {
                "name": "ema_slow_v",
                "type": "choice",
                "value_type": "int",
                "values": [21, 28, 32, 45, 50],
            },
            {
                "name": "prediction_index",
                "type": "choice",
                "value_type": "int",
                "values": [4, 5, 6, 7, 8, 9, 10],
            },
        ],
        # Booth function
        evaluation_function=lambda v: evaluate_moving_avg(
            number_of_twisted_points=int(v["number_of_twisted_points"]),
            from_last_twisted_point_to_forward=int(v["from_last_twisted_point_to_forward"]),
            direction_error=float(v["direction_error"]),
            consecutive_error=float(v["consecutive_error"]),
            ema_fast_v=int(v["ema_fast_v"]), ema_slow_v=int(v["ema_slow_v"]),
            prediction_index=int(v["prediction_index"]),
        ),
        minimize=False,
    )

    print(best_parameters)
# {'x1': 1.02, 'x2': 2.97}  # true min is (1, 3)
