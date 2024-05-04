from pathlib import Path
from mdframe.reader import run, Config
import pandas as pd

def check_df(df: pd.DataFrame, query: str, contain_list: list[str]) -> bool:
    """Checks if the dataframe satisfies the given parameters
    
    Args:
        df (pd.DataFrame): The dataframe to be checked
        query (str): The query to filter the dataframe
        contain_list (list[str]): The list of strings that the dataframe should contain
    Return:
        bool: True if the dataframe satisfies the given parameters, False otherwise
    """
    
    satisfied = False

    for row in range(df.shape[0]):
        for col in range(df.shape[1]):
            if type(df.iloc[row, col]) == list:
                for item in df.iloc[row, col]:
                    if item in contain_list:
                        satisfied = True

    columns = list(df.columns)[2:]
    df["combined"] = df.apply(lambda row: ''.join(str(row[col]) if str(row[col]) != "nan" else "" for col in columns), axis=1)
    df = df.drop(columns=columns)
    df = df.transpose()

    if query != "":
        if not df.query(query).empty:
            satisfied = True

    return satisfied

def filter_files(data_path: str, file_type: str, query: str="", contain_list: list[str]=[]) -> list[str]:
    
    """Filters the dataframes based on the given parameters
    
    Args:
        data_path (str): The data directory path
        file_type (str): The file type
        query (str): The query to filter the dataframe
        contain_list (list[str]): The list of strings that the dataframe should contain
    Return:
        list[str]: The list of satisfied files
    """

    config = Config(data_path, file_type)
    df_list = run(config)
    satisfied_files = []
    
    for df in df_list:
        if check_df(df, query, contain_list):
            satisfied_files.append(df.iloc[0,0])
    
    return sorted(satisfied_files)


if __name__ == "__main__":
    data_path = Path(__file__).parent.parent / "sample toml files"
    file_type = "toml"

    print(filter_files(data_path, file_type, query='weight == "321"') == [51])
    print(filter_files(data_path, file_type, query='started=="test" and weight == "321"') == [])
    print(filter_files(data_path, file_type, query='started=="test" or weight == "321"') == [51])
    print(filter_files(data_path, file_type, query="started == '15:02:33' and weight == '22'") == [52])
    print(filter_files(data_path, file_type, query="started == '15:02:33' and weight == '22'", contain_list=["IMG_4166"])==[52, 53])
    
    
    