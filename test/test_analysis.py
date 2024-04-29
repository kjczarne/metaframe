import unittest
from pathlib import Path
from mdframe.reader import run, Config
from mdframe.analysis import flatten_property_dict, load_flattened_data, filter_data, generate_histogram
import pandas as pd
import toml

class TestAnalysis(unittest.TestCase):

    def test_flatten_property_dict(self):
        test_data_path = Path(__file__).parent / "data"
        flattened_data_path = Path(__file__).parent / "flattened_data"

        # first test
        with open(test_data_path / "00_input_file.toml", 'r') as f:
            input_file_0 = toml.load(f)
        with open(flattened_data_path / "00_flattened_file.toml", 'r') as f:
            output_file_0 = toml.load(f)
        assert flatten_property_dict(input_file_0) == output_file_0

        # second test
        with open(test_data_path / "01_input_file.toml", 'r') as f:
            input_file_1 = toml.load(f)
        with open(flattened_data_path / "01_flattened_file.toml", 'r') as f:
            output_file_1 = toml.load(f)
        assert flatten_property_dict(input_file_1) == output_file_1
        
        # third test
        with open(test_data_path / "02_input_file.toml", 'r') as f:
            input_file_2 = toml.load(f)
        with open(flattened_data_path / "02_flattened_file.toml", 'r') as f:
            output_file_2 = toml.load(f)
        assert flatten_property_dict(input_file_2) == output_file_2

    def test_load_flatten_data(self):
        config = Config(
            data_path=Path(__file__).parent / "data", 
            metadata_file_extension="toml", 
            schema_loc=Path('../src/mdframe/schema.json')
        )

        # create a dataframe using the method
        first_df = load_flattened_data(config)

        # create an identical dataframe by manually accessing the equivalent flattened_data files
        flattened_data_path = Path(__file__).parent / "flattened_data"
        files = []
        for file in list(flattened_data_path.iterdir()):
            with open(flattened_data_path / file, 'r') as f:
                files.append(toml.load(f))
        second_df = pd.DataFrame.from_dict(files)

        assert first_df.equals(second_df)

    def test_filter_data(self):
        filtered_data_filename = 'filtered_data.csv'
        filtered_data_file_path = Path(__file__).parent / filtered_data_filename

        # delete file if persists from previous run
        if filtered_data_file_path.exists():
            filtered_data_file_path.unlink()

        config = Config(
            data_path=Path(__file__).parent / "data", 
            metadata_file_extension="toml", 
            schema_loc=Path('../src/mdframe/schema.json')
        )

        # test 1
        filter_data(config, query='df["gid"] >= 66', filename=filtered_data_filename)
        df = pd.read_csv(filtered_data_file_path, index_col=0)
        assert len(df.index) == 2

        # test 2
        filter_data(config, query='df["nutrition_subgroup"] == "nachos"', filename=filtered_data_filename)        
        df = pd.read_csv(filtered_data_file_path, index_col=0)
        assert len(df.index) == 1 and df.iloc[0]['gid'] == 75

        # test 3
        filter_data(config, query='df["quality"] == 1', filename=filtered_data_filename)
        df = pd.read_csv(filtered_data_file_path, index_col=0)
        assert len(df.index) == 0

        # delete file if persists before next run
        if filtered_data_file_path.exists():
            filtered_data_file_path.unlink()

    def generate_histogram(self):
        pass

if __name__ == "__main__":
    unittest.main()
