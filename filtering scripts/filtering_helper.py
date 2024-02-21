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

    """Filter the dataframes based on the given parameters for AND condition
    
    Args::
        df_list -- the list of dataframes
        kwargs -- the parameters
    Return:
        list[str]: The list of satisfied files
    """

    statisfied_files = []

    for df in df_list:
        check_if_satisfied = True
        for key, arg in kwargs.items():
            if key not in list(df.index):
                print(key + " is not a valid parameter")
                continue
            
            row = list(df.loc[key,:].values)
            if type(arg) == list:
                check_if_satisfied = False
                for sub_arg in arg:
                    if check_existence(sub_arg, row):
                        check_if_satisfied = True
            elif not check_existence(arg, row):
                check_if_satisfied = False
        
        if check_if_satisfied:
            statisfied_files.append(df.loc["nutrition_subgroup", "gid"])
    
    return sorted(statisfied_files)

def filter_files_or(df_list: str,  **kwargs) -> list[str]:
    """Filter the dataframes based on the given parameters for OR condition
    
    Args::
        df_list -- the list of dataframes
        kwargs -- the parameters
    Return:
        list[str]: The list of satisfied files
    """
    
    statisfied_files = []

    for df in df_list:
        check_if_satisfied = False
        for key, arg in kwargs.items():
            if key not in list(df.index):
                print(key + " is not a valid parameter")
                continue
            
            row = list(df.loc[key,:].values)
            if type(arg) == list:
                for sub_arg in arg:
                    if check_existence(sub_arg, row):
                        check_if_satisfied = True
                        break
            elif check_existence(arg, row):
                check_if_satisfied = True
                break
        
        if check_if_satisfied:
            statisfied_files.append(df.loc["nutrition_subgroup", "gid"])
    
    return sorted(statisfied_files)