import unittest
import location
import numpy as np

class MyTestCase(unittest.TestCase):


    def test_multilaterate(self):

        # Define the beacon locations
        beacon_locs = np.array([[0, 0], [3, 0], [0, 4], [3, 4]])

        # Define the true location of the student
        true_location = np.array([1.5, 2])

        # Calculate the true distances from the student to each beacon
        true_distances = np.sqrt(np.sum((beacon_locs - true_location)**2, axis=1))

        # Calculate the true RSSI values from the student to each beacon
        true_rssi = -55 - 10 * 2 * np.log10(true_distances)

        # Add some noise to the RSSI values
        rssi_noise = np.random.normal(0, 2, size=beacon_locs.shape[0])
        rssi_values = true_rssi + rssi_noise

        # Call the multilaterate function to estimate the location of the student
        estimated_location = location.multilaterate(beacon_locs, rssi_values)

        # Check that the estimated location is close to the true location
        self.assertTrue(np.allclose(estimated_location, true_location, rtol=0.1))


if __name__ == '__main__':
    unittest.main()
