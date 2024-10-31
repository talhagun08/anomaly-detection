import unittest
from main import detect_anomaly

class TestAnomalyDetection(unittest.TestCase):

    def test_no_anomalies(self):
        data = [10, 12, 11, 9, 10, 11, 12, 10, 11]  # Normal data set
        is_anomaly, moving_avg = detect_anomaly(data)
        self.assertFalse(is_anomaly, "There should be no anomaly.")
        self.assertIsNotNone(moving_avg, "Moving average should be calculated.")

    def test_anomaly_detected(self):
        data = [10, 12, 11, 9, 10, 100]  # 100 is a clear anomaly
        is_anomaly, moving_avg = detect_anomaly(data)
        self.assertTrue(is_anomaly, "Anomaly should have been detected.")
        self.assertIsNotNone(moving_avg, "Moving average should be calculated.")

    def test_insufficient_data(self):
        """ Anomaly should not be detected if there is insufficient data. """
        data = [10]  # Insufficient data
        is_anomaly, moving_avg = detect_anomaly(data)
        self.assertFalse(is_anomaly, "There should be no anomaly with insufficient data.")
        self.assertIsNone(moving_avg, "Average should not be calculated due to insufficient data.")

if __name__ == '__main__':
    unittest.main()
