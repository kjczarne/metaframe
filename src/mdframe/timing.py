"""This scripts provides facilities for calculating and aggregating timing information
for data capture processes.
"""

import time
import pandas as pd
from typing import Callable, Tuple, Any, Iterable


def calc_time(start: time.time, end: time.time) -> float:
    """Calculates the time between two time.time() calls.
    
    Args:
        start (time.time): The start time
        end (time.time): The end time
    
    Returns:
        float: The time difference in seconds
    """
    return end - start


def calc_rate(time_delta: float, count: int) -> float:
    """Calculates the rate of a process given the time and the count.
    
    Args:
        time (float): The time in seconds
        count (int): The count of the process
    
    Returns:
        float: The rate of the process
    """
    return count / time_delta


def calc_time_and_rate(start: time.time,
                       end: time.time,
                       count: int) -> (float, float):
    """Calculates the time and the rate of a process given the start and end time and the count.
    
    Args:
        start (time.time): The start time
        end (time.time): The end time
        count (int): The count of the process
    
    Returns:
        (float, float): The time and the rate of the process
    """
    time_delta = calc_time(start, end)
    rate = calc_rate(time_delta, count)
    return time_delta, rate


def calc_time_row(row: pd.Series,
                 time_getter: Callable[[pd.Series], Tuple[time.time, time.time]]) -> float:
    """Calculates the time delta for each row in a dataframe (for each sample collected).
    The time delta is returned as seconds

    Args:
        row (pd.Series): a row in a dataframe containing the start and end time (a sample)
        time_getter (Callable[[Any], Tuple[time.time, time.time]]): a function which selects
            the start and end time from a row in the dataframe
    """

    start, end = time_getter(row)
    time_delta = calc_time(start, end)
    return time_delta


def calc_time_and_rate_from_a_generic_df(df: pd.DataFrame | Iterable[pd.DataFrame],
                                         time_column_name: str = "time",
                                         start_key: str = "start",
                                         end_key: str = "end") -> (float, float):
    """Caclulates time and rate from a dataframe containing a `time` column
    with `start` and `end` sub-keys.

    Args:
        df (pd.DataFrame): a generic dataframe with a `time` column containing
            start and end sub-keys
        scale (str): [NumPy datetime64 unit](https://numpy.org/doc/stable/reference/arrays.datetime.html#datetime-units)

    Returns:
        (float, float): total time taken and rate per second
    """
    if isinstance(df, pd.DataFrame):
        starts = df[time_column_name].map(lambda x: x[start_key]).astype('datetime64[ns]')
        ends = df[time_column_name].map(lambda x: x[end_key]).astype('datetime64[ns]')
        deltas = ends - starts
        return deltas.sum(), calc_rate(deltas.sum().total_seconds(), len(deltas))
    elif isinstance(df, Iterable):
        total_time = 0
        total_count = 0
        for d in df:
            starts = pd.Series(d[time_column_name][start_key]).astype('datetime64[ns]')
            ends = pd.Series(d[time_column_name][end_key]).astype('datetime64[ns]')
            deltas = ends - starts
            total_time += deltas.sum().total_seconds()
            total_count += len(deltas)
        return total_time, calc_rate(total_time, total_count)
    else:
        raise ValueError("df must be a pandas DataFrame or an iterable of DataFrames")
