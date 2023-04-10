import math
from scipy.optimize import least_squares


def rssi_to_meters(rssi):
    txPower = -65
    ratio = rssi * 1.0 / txPower
    if ratio < 1.0:
        return math.pow(ratio, 10)
    else:
        return math.pow((-rssi / (10 * 2)), 10)


def trilateration(beacon_list, rssi_list):
    # Convert RSSI readings to distances in meters
    d_list = [rssi_to_meters(rssi) for rssi in rssi_list]

    # Define the trilateration equations
    def fun(p):
        x_list = [beacon[0] for beacon in beacon_list]
        y_list = [beacon[1] for beacon in beacon_list]
        return [(x - p[0]) ** 2 + (y - p[1]) ** 2 - d ** 2 for x, y, d in zip(x_list, y_list, d_list)]

    # Solve the trilateration equations using least squares
    res = least_squares(fun, [0, 0])

    # Return laptop location
    return res.x[0], res.x[1]
