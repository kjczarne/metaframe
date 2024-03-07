import unittest
from pathlib import Path
from mdframe.reader import run, Config
from mdframe.schema import schema

class TestReader(unittest.TestCase):

    def test_metadata_print(self):
        data_dir_path = Path(__file__).parent / "data_dir"
        config = Config(data_dir_path, "toml", schema)
        df = run(config)
        print(df)

if __name__ == "__main__":
    unittest.main()
