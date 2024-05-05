import unittest
from pathlib import Path
from typing import Tuple
from mdframe.reader import run, Config
from mdframe.analysis import flatten_property_dict, load_flattened_data, filter_data, generate_histogram
import pandas as pd
import toml

root = Path(__file__).parent


class TestAnalysis(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.schema_loc = root / "../src/mdframe/schema.json"
        cls.test_data_path = Path(__file__).parent / "data"
        cls.flattened_data_path = Path(__file__).parent / "flattened_data"
        cls.filtered_data_filename = 'filtered_data.csv'
        cls.filtered_data_file_path = Path(__file__).parent / cls.filtered_data_filename
        cls.representation = "raw"

    def flatten_property_dict_test_factory(self, file_idx: int):
        input_file = self.test_data_path / f"{file_idx:02}_input_file.toml"
        output_file = self.flattened_data_path / f"{file_idx:02}_flattened_file.toml"
        with open(input_file, 'r') as f:
            input_file = toml.load(f)
        with open(output_file, 'r') as f:
            output_file = toml.load(f)
        self.assertDictEqual(flatten_property_dict(input_file), output_file)


    def test_flatten_property_dict(self):
        for i in range(0, 2):
            with self.subTest(i=i):
                self.flatten_property_dict_test_factory(i)


    @unittest.skip("This test is failing, needs to be fixed.")
    def test_load_flatten_data(self):
        config = Config(
            metadata_file_paths=self.test_data_path, 
            metadata_file_extension="toml", 
            schema_loc=self.schema_loc,
            representation=self.representation
        )

        # create a dataframe using the method
        first_df = load_flattened_data(config)

        # create an identical dataframe by manually accessing the equivalent flattened_data files
        flattened_data_path = Path(__file__).parent / "flattened_data"
        files = []
        for file in flattened_data_path.iterdir():
            with open(flattened_data_path / file, 'r') as f:
                files.append(toml.load(f))
        second_df = pd.DataFrame.from_dict(files)

        assert first_df.equals(second_df)

    def delete_filtered_data_file(self):
        if self.filtered_data_file_path.exists():
            self.filtered_data_file_path.unlink()

    def filter_data_test_factory(self,
                                 config: Config,
                                 query: str,
                                 expected_length: int,
                                 gid_assert: Tuple[int, int] | None = None):
        filter_data(config, query=query, filename=self.filtered_data_file_path)
        df = pd.read_csv(self.filtered_data_file_path, index_col=0)
        self.assertEqual(len(df.index), expected_length)
        if gid_assert:
            row_idx, expected_gid = gid_assert
            self.assertEqual(df.iloc[row_idx]['gid'], expected_gid)

    def test_filter_data(self):
        # delete file if persists from previous run
        self.delete_filtered_data_file()

        config = Config(
            metadata_file_paths=self.test_data_path, 
            metadata_file_extension="toml", 
            schema_loc=self.schema_loc,
            representation=self.representation
        )

        test_params = [
            ('df["gid"] >= 66', 2, None),
            ('df["nutrition_subgroup"] == "nachos"', 1, (0, 75)),
            ('df["quality"] == 1', 0, None)
        ]

        for query, expected_length, gid_assert in test_params:
            with self.subTest(query=query):
                self.filter_data_test_factory(config, query, expected_length, gid_assert)

        # delete file if persists before next run
        self.delete_filtered_data_file()

    @unittest.skip("Histogram generation does not require testing at this time.")
    def generate_histogram(self):
        pass


if __name__ == "__main__":
    unittest.main()
