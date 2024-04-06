import unittest
from pathlib import Path
from mdframe.reader import run, Config
import json
import toml

class TestReader(unittest.TestCase):

    def test_metadata_print(self):
        data_dir_path = Path(__file__).parent / "data_dir"
        schema_loc = Path('../src/mdframe/schema.json')
        config = Config(
            data_dir_path=data_dir_path, 
            metadata_file_extension="toml", 
            schema_loc=schema_loc
        )
        df = run(config)
        print(df)

    def test_metadata_invalid(self):
        data_dir_path = Path(__file__).parent / "invalid_data_dir"
        schema_loc = Path('../src/mdframe/schema.json')
        config = Config(
            data_dir_path=data_dir_path, 
            metadata_file_extension="toml", 
            schema_loc=schema_loc
        )

        # expecting this to fail
        try:
            df = run(config)
            print(df)
        except:
            pass

if __name__ == "__main__":
    unittest.main()
