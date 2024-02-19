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

def filter_files(data_dir_path: str, file_type: str,  **kwargs) -> list[str]:
    
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

    satisfied_files = []
    for df in df_list:
        check_if_satisfied = False
        for key, arg in kwargs.items():
            if key not in list(df.index):
                print(key + " is not a valid parameter")
                continue

            row = list(df.loc[key,:].values)

            # if the arg is a list, check if all the items in the list exist in the row
            if type(arg) == list:
                condition_or = False
                for item in arg:
                    condition_and = True
                    if type(item) == list:
                        # if the item is a list, check if all the sub_items in the list exist in the row
                        for sub_item in item:
                            if not check_existence(sub_item, row):
                                condition_and = False
                    
                    if condition_and and type(item) == list:
                        condition_or = True

                    elif check_existence(item, row):
                        condition_or = True
                if condition_or:
                    check_if_satisfied = True

            # if the arg is not a list, check if the arg exists in the row
            elif check_existence(arg, row):
                check_if_satisfied = True

        # To prevent adding the same file multiple times
        if check_if_satisfied:
            satisfied_files.append(df.loc["nutrition_subgroup", "gid"])

    return sorted(satisfied_files)


if __name__ == "__main__":
    data_dir_path = Path(__file__).parent.parent / "sample toml files"
    file_type = "toml"

    print(filter_files(data_dir_path, file_type, started="15:02:33") == [52])
    print(filter_files(data_dir_path, file_type, texture_sources="IMG_7088") == [52])
    # 1 bracket is condition or, 2 brackets is condition and
    print(filter_files(data_dir_path, file_type, texture_sources=["IMG_7082"]) == [51])
    print(filter_files(data_dir_path, file_type, texture_sources=["IMG_7088"]) == [52])
    print(filter_files(data_dir_path, file_type, texture_sources=[["IMG_7088"], ["IMG_7082"]]) == [51, 52])

    # This is condition and
    print(filter_files(data_dir_path, file_type, weight = 160, quality_comments = "great individual scans, unable to merge")==[48])
    
    