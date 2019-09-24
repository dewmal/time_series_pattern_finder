def is_rectangle(x_pos, y_pos, error_allowed):
    a_x, b_x, c_x, d_x, e_x = x_pos
    a_y, b_y, c_y, d_y, e_y = y_pos
    M1 = c_x - e_x / c_y - e_y
    M2 = b_x - d_x / b_y - d_y

    accept_range = [1 - error_allowed, 1 + error_allowed]
    m1_m2_diff = M1 / M2
    if accept_range[0] < m1_m2_diff < accept_range[1]:
        if a_y < b_y < c_y and a_y < d_y < e_y:
            return 1
        elif a_y > c_y > b_y and a_y > e_y > d_y:
            return -1


def is_wedge(x_pos, y_pos, error_allowed=0.0):
    a_x, b_x, c_x, d_x, e_x = x_pos
    a_y, b_y, c_y, d_y, e_y = y_pos
    M1 = c_x - e_x / c_y - e_y
    M2 = b_x - d_x / b_y - d_y

    # accept_range = [1 - error_allowed, 1 + error_allowed]

    if (M2 > 0 and M1 > 0) or (M1 < 0 and M1 < 0):
        if a_y < b_y < c_y and a_y < d_y < e_y:
            return 1
        elif a_y > c_y > b_y and a_y > e_y > d_y:
            return -1


def is_pennant(x_pos, y_pos, error_allowed=0.0):
    a_x, b_x, c_x, d_x, e_x = x_pos
    a_y, b_y, c_y, d_y, e_y = y_pos
    M1 = c_x - e_x / c_y - e_y
    M2 = b_x - d_x / b_y - d_y

    # accept_range = [1 - error_allowed, 1 + error_allowed]

    if (M1 > 0 > M2) or (M1 < 0 < M2):
        if a_y < b_y < c_y and a_y < d_y < e_y:
            return 1
        elif a_y > c_y > b_y and a_y > e_y > d_y:
            return -1
