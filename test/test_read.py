import unittest
from pathlib import Path
from mdframe.reader import run, Config
import json
import toml

root = Path(__file__).parent


class TestReader(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.schema_loc = root / "../src/mdframe/schema.json"

    def test_metadata_print(self):
        data_path = root / "test"
        config = Config(
            data_path=data_path,
            metadata_file_extension="toml",
            schema_loc=self.schema_loc
        )
        df = run(config)
        print(df)

    def test_metadata_invalid(self):
        data_path = Path(__file__).parent / "invalid_data"
        config = Config(
            data_path=data_path,
            metadata_file_extension="toml",
            schema_loc=self.schema_loc
        )

        # expecting this to fail
        with self.assertRaises(toml.decoder.TomlDecodeError):
            df = run(config)

if __name__ == "__main__":
    unittest.main()
