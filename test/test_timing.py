import unittest
import pandas as pd
from mdframe.timing import calc_time_and_rate_from_a_generic_df


class TestTiming(unittest.TestCase):

    def test_calc_time_and_rate_from_a_generic_df(self):
        df = pd.DataFrame({
            "time": [
                {"start": "2022-01-01 00:00:00", "end": "2022-01-01 00:00:10"},
                {"start": "2022-01-01 00:00:10", "end": "2022-01-01 00:00:20"},
                {"start": "2022-01-01 00:00:20", "end": "2022-01-01 00:00:30"}
            ]
        })
        total_time, rate = calc_time_and_rate_from_a_generic_df(df)
        self.assertEqual(total_time.total_seconds(), 30.0)
        self.assertAlmostEqual(rate, 0.1)

if __name__ == "__main__":
    unittest.main()
