import unittest
from pathlib import Path
from mdframe.reader import run, Config
from mdframe.analysis import flatten_property_dict, load_flattened_data, filter_data, generate_histogram
import pandas as pd
import toml

class TestAnalysis(unittest.TestCase):

    def test_flatten_property_dict(self):
        # first test
        test_0_path = Path(__file__).parent / "data" / "test_0"
        with open(test_0_path / "input_file.toml", "r") as f:
            input_file_0 = toml.load(f)
        with open(test_0_path / "output_file.toml", "r") as f:
            output_file_0 = toml.load(f)
        assert flatten_property_dict(input_file_0) == output_file_0

        # second test
        test_1_path = Path(__file__).parent / "data" / "test_1"
        with open(test_1_path / "input_file.toml", "r") as f:
            input_file_1 = toml.load(f)
        with open(test_1_path / "output_file.toml", "r") as f:
            output_file_1 = toml.load(f)
        assert flatten_property_dict(input_file_1) == output_file_1
        
        # third test
        test_2_path = Path(__file__).parent / "data" / "test_2"
        with open(test_2_path / "input_file.toml", "r") as f:
            input_file_2 = toml.load(f)
        with open(test_2_path / "output_file.toml", "r") as f:
            output_file_2 = toml.load(f)

        assert flatten_property_dict(input_file_2) == output_file_2

    def test_filter_data(self):
        pass

    def generate_histogram(self):
        pass

if __name__ == "__main__":
    unittest.main()
