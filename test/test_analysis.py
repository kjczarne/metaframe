import unittest
from pathlib import Path
from mdframe.reader import run, Config
from mdframe.analysis import load_flattened_data, filter_data, generate_histogram
import pandas as pd

class TestAnalysis(unittest.TestCase):

    def test_load_flattened_data(self):
        config = Config(
            data_path = Path(__file__).parent / "data" / "input", 
            metadata_file_extension = "toml",
            schema_loc = Path('../src/mdframe/schema.json')
        )

        df = load_flattened_data(config)
        df.to_csv('data/output/output_file_0.csv')
        print(df)

        # test 1
        ans_df = pd.read_csv('data/ans/output_file_0.csv')
        # ans_df = pd.read_csv('data/ans/ans_file.csv', index_col=0)

        print(df)
        print('------------')
        print(ans_df)

        # assert df.equals(ans_df)
        # ans_df.to_csv('asdf')

        # f = pd.read_csv('asdf')
        # # assert f.equals(ans_df)
        # assert ans_df.equals(df)

    def test_filter_data(self):
        pass

    def generate_histogram(self):
        pass

if __name__ == "__main__":
    unittest.main()
