import unittest
from pathlib import Path
from mdframe.reader import run, Config
import json
class TestReader(unittest.TestCase):

    def test_metadata_print(self):
        data_dir_path = Path(__file__).parent / "data_dir"
        config = Config(
            data_dir_path=data_dir_path, 
            metadata_file_extension="toml", 
            schema_url='../src/mdframe/schema.json'
        )
        df = run(config)
        print(df)

if __name__ == "__main__":
    unittest.main()
