from pathlib import Path
from mdframe.reader import run, Config
import pandas as pd

def check_existence(arg: str, row: str) -> bool:

    """Check if the arg exist to the row
    
    Args::
        arg -- the arg to check
        row -- the row to check
    Return:
        bool: True if the arg exists in the row, False otherwise
    """
    
    for item in row:
        if type(item) == list and arg in item:
            return True
        
        if arg == item:
            return True
        
    return False

def filter_files_and(df_list: str,  **kwargs) -> list[str]:

    statisfied_files = []

    for df in df_list:
        check_if_satisfied = True
        for key, arg in kwargs.items():
            if key not in list(df.index):
                print(key + " is not a valid parameter")
                continue
            
            row = list(df.loc[key,:].values)
            if not check_existence(arg, row):
                check_if_satisfied = False
        
        if check_if_satisfied:
            statisfied_files.append(df.loc["nutrition_subgroup", "gid"])
    
    return sorted(statisfied_files)

def filter_files_or(df_list: str,  **kwargs) -> list[str]:
    statisfied_files = []

    for df in df_list:
        check_if_satisfied = False
        for key, arg in kwargs.items():
            if key not in list(df.index):
                print(key + " is not a valid parameter")
                continue
            
            row = list(df.loc[key,:].values)
            if check_existence(arg, row):
                check_if_satisfied = True
        
        if check_if_satisfied:
            statisfied_files.append(df.loc["nutrition_subgroup", "gid"])
    
    return sorted(statisfied_files)


def filter_files(data_dir_path: str, file_type: str, condition_and: bool,  **kwargs) -> list[str]:
    
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

    print(filter_files(data_dir_path, file_type, condition_and=True, started="15:02:33") == [52])
    print(filter_files(data_dir_path, file_type, condition_and=True, texture_sources="IMG_7088") == [52])
    print(filter_files(data_dir_path, file_type, condition_and=False, weight = 160, quality_comments = "great individual scans, unable to merge")==[48])
    
    