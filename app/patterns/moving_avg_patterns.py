import numpy as np


def moving_average_signal(values, sma_one, sma_two, number_of_twisted_points=3, from_last_twisted_point_to_forward=3,
                          consecutive_error=10 / 100, direction_error=10 / 100):
    x_point = np.nan
    diffs_in_there = np.array(sma_one > sma_two)
    twisted_points = []
    for idx in range(1, len(diffs_in_there)):
        if diffs_in_there[idx - 1] != diffs_in_there[idx]:
            twisted_points.append(idx)
            if len(twisted_points) > number_of_twisted_points:
                break
    if len(twisted_points) >= number_of_twisted_points:
        twisted_points = np.array(twisted_points)
        x_point = twisted_points[-1]
        consider_line_x_range = np.array([idx for idx in range(x_point, len(values) - 1)])

        if len(consider_line_x_range) > from_last_twisted_point_to_forward:
            last_diffs = (sma_one[consider_line_x_range] - sma_two[consider_line_x_range]) * 100 / np.max(values)

            consecutives = []
            for ivx in range(1, len(last_diffs)):
                diff = last_diffs[ivx - 1] / last_diffs[ivx]
                consecutives.append(diff < 1)
            consecutives = np.array(consecutives)
            consecutive_avg = len(np.where(consecutives == True)[0]) * 100 / len(consecutives)
            # print(consecutive_avg)
            # if consecutive:
            if consecutive_avg >= 100 - consecutive_error:
                direction_avg = len(np.where(last_diffs > 0)[0]) * 100 / len(last_diffs)
                if direction_avg >= 100 - direction_error:
                    # title += "Bullish Patterns"
                    return 1, x_point
                elif direction_avg <= direction_error:
                    # title += "Bearish Patterns"
                    return -1, x_point
    return np.nan, x_point
