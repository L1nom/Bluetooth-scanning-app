import numpy as np
from scipy.optimize import least_squares

def rssi_to_distance(rssi, tx_power, n):
    return 10 ** ((tx_power - rssi) / (10 * n))

def trilateration(beacons, rssi_readings):
    tx_power, n = -65, 2
    def objective_func(x, beacons, distances):
        return [(np.sqrt((x[0] - beacon[0]) ** 2 + (x[1] - beacon[1]) ** 2) - distance) for beacon, distance in zip(beacons, distances)]

    distances = [rssi_to_distance(rssi, tx_power, n) for rssi in rssi_readings]
    distances = [3.0567, 3.1313, 3.6629 , 3.7189]
    initial_guess = np.mean(beacons, axis=0)
    res = least_squares(objective_func, initial_guess, args=(beacons, distances))
    return res.x[0], res.x[1]

# Example usage
# D C E F
# beacon_list = [(6.2587, 3.12), (1.524, 3.12), (6.2587, 7.7362), (1.524,7.7362)]

# rssi_list = [-73, -60, -73, -75]
# # tx_power = -65 # Example TxPower at 1 meter
# # n = 2  # Example path loss exponent

# object_location = trilateration(beacon_list, rssi_list)
# print(object_location)