import unittest
from pathlib import Path
from mdframe.reader import run_eager, Config
import json
import toml

root = Path(__file__).parent


class TestReader(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.schema_loc = root / "../src/mdframe/schema.json"

    def test_metadata_loads(self):
        data_path = root / "data"
        config = Config(
            metadata_file_paths=data_path,
            metadata_file_extension="toml",
            schema_loc=self.schema_loc
        )
        df = run_eager(config)
        self.assertGreater(len(df), 0)

    def test_metadata_invalid_raises_decoding_error(self):
        data_path = Path(__file__).parent / "invalid_data"
        config = Config(
            metadata_file_paths=data_path,
            metadata_file_extension="toml",
            schema_loc=self.schema_loc
        )

        # expecting this to fail
        with self.assertRaises(toml.decoder.TomlDecodeError):
            _ = run_eager(config)

if __name__ == "__main__":
    unittest.main()
