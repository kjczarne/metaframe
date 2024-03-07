import unittest
from pathlib import Path
from mdframe.reader import run, Config, flatten_property_dict


class TestReader(unittest.TestCase):

    def test_metadata_print(self):
        data_dir_path = Path(__file__).parent / "data_dir"
        config = Config(data_dir_path, "toml")
        df = run(config)
        print(df)

    def test_flatten_property_dict(self):
        input = {'gid': 50, 
          'uid': 'f1e75821-e41f-4159-9050-def0d981b648', 
          'item': 
            {'nutrition_subgroup': 'ice cream and frozen dairy desserts', 'food_type': 'ice cream', 'description': 'Kawartha Death by Chocolate ice cream made with fresh milk and cream'}, 
          'metrics': 
            {'weight': 101, 'unit': 'g', 'ingredients': []}, 
          'model': 
            {'project_name': 'Project11192023134625', 'rgbd_file_names': ['50_icecream_1'],      'nutrition_facts_sources': ['IMG_7055', 'IMG_7056', 'IMG_7057'], 'texture_sources': ['IMG_7064', 'IMG_7065', 'IMG_7066', 'IMG_7067'], 'quality': 3, 'quality_comments': 'some minor holes near plate were filled, otherwise great detail'}, 
          'time': 
            {'started': '13:43:56', 'finished': '13:57:25'}}
        desired_output = {'gid': 50, 
          'uid': 'f1e75821-e41f-4159-9050-def0d981b648', 
          'nutrition_subgroup': 'ice cream and frozen dairy desserts', 
          'food_type': 'ice cream', 'description': 'Kawartha Death by Chocolate ice cream made with fresh milk and cream', 'weight': 101, 'unit': 'g', 'ingredients': [], 
          'project_name': 'Project11192023134625', 'rgbd_file_names': ['50_icecream_1'],      'nutrition_facts_sources': ['IMG_7055', 'IMG_7056', 'IMG_7057'], 'texture_sources': ['IMG_7064', 'IMG_7065', 'IMG_7066', 'IMG_7067'], 'quality': 3, 'quality_comments': 'some minor holes near plate were filled, otherwise great detail', 'started': '13:43:56', 'finished': '13:57:25'}
        assert desired_output == flatten_property_dict(input)


if __name__ == "__main__":
    unittest.main()
