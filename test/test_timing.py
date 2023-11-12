import pytest
import pandas as pd
from mdframe.timing import calc_time_and_rate_from_a_generic_df


def test_calc_time_and_rate_from_a_generic_df():
    df = pd.DataFrame({
        "time": [
            {"start": "2022-01-01 00:00:00", "end": "2022-01-01 00:00:10"},
            {"start": "2022-01-01 00:00:10", "end": "2022-01-01 00:00:20"},
            {"start": "2022-01-01 00:00:20", "end": "2022-01-01 00:00:30"}
        ]
    })
    total_time, rate = calc_time_and_rate_from_a_generic_df(df)
    assert total_time == 30.0
    assert rate == 1.0

if __name__ == "__main__":
    pytest.main()
