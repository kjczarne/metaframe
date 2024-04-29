import unittest
from pathlib import Path
from mdframe.reader import run, Config
import json
import toml

class TestReader(unittest.TestCase):

    def test_metadata_print(self):
        data_path = Path(__file__).parent / "test"
        schema_loc = Path('../src/mdframe/schema.json')
        config = Config(
            data_path=data_path, 
            metadata_file_extension="toml", 
            schema_loc=schema_loc
        )
        df = run(config)
        print(df)

    @unittest.expectedFailure
    def test_metadata_invalid(self):
        data_path = Path(__file__).parent / "invalid_data"
        schema_loc = Path('../src/mdframe/schema.json')
        config = Config(
            data_path=data_path, 
            metadata_file_extension="toml", 
            schema_loc=schema_loc
        )

        # expecting this to fail
        try:
            df = run(config)
            print(df)
        except:
            pass

        with self.assertRaises(TypeError):  
            s.split(2)

if __name__ == "__main__":
    unittest.main()
