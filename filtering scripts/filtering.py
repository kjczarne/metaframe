from pathlib import Path
from mdframe.reader import run, Config
import pandas as pd
from filtering_helper import filter_files_and, filter_files_or, check_existence


def filter_files(data_dir_path: str, file_type: str, condition_and: bool = True,  **kwargs) -> list[str]:
    
    """Filters the dataframes based on the given parameters
    
    Args:
        data_dir_path (str): The data directory path
        file_type (str): The file type
        kwargs: The parameters
    Return:
        list[str]: The list of satisfied files
    """

    config = Config(data_dir_path, file_type)
    df_list = run(config)

    if condition_and:
        satisfied_files = filter_files_and(df_list, **kwargs)
    else:
        satisfied_files = filter_files_or(df_list, **kwargs)

    return sorted(satisfied_files)


if __name__ == "__main__":
    data_dir_path = Path(__file__).parent.parent / "sample toml files"
    file_type = "toml"

    # if condition_and is True, then file must satisfy all arguments 
    print(filter_files(data_dir_path, file_type, condition_and=True, weight = 321, started="14:38:34") == [51])
    print(filter_files(data_dir_path, file_type, condition_and=True, weight = 321, started="14:38:33") == [])
    print(filter_files(data_dir_path, file_type, condition_and=False, weight = 321, started="14:38:34") == [51])

    # if argument is a list, then file must satisfy at least one of the arguments in the list
    print(filter_files(data_dir_path, file_type, condition_and=True, texture_sources="IMG_7088") == [52])
    print(filter_files(data_dir_path, file_type, condition_and=True, texture_sources=["IMG_7088", "IMG_4167"]) == [52, 53])
    
    