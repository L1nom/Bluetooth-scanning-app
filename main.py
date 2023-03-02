import numpy as np


def multilaterate(beacon_locs, rssi_values):
    # Define the function for calculating distance from RSSI values
    def rssi_to_distance(rssi, n, a):
        return 10**((a-rssi)/(10*n))

    # Define the number of beacons
    num_beacons = beacon_locs.shape[0]

    # Initialize variables for A and b matrices
    A = np.zeros((num_beacons - 1, 2))
    b = np.zeros((num_beacons - 1, 1))

    # Calculate A and b matrices
    for i in range(num_beacons - 1):
        A[i, :] = beacon_locs[i + 1, :] - beacon_locs[0, :]
        b[i] = rssi_to_distance(rssi_values[0], 2, -55)**2 - rssi_to_distance(rssi_values[i + 1], 2, -55)**2 + np.sum(beacon_locs[i + 1, :]**2) - np.sum(beacon_locs[0, :]**2)

    # Solve for x and y using least squares
    xy = np.linalg.lstsq(A, b, rcond=None)[0]

    # Return the estimated x and y coordinates of the student
    return xy.flatten()
