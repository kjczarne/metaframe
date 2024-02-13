from pathlib import Path
from mdframe.reader import run, Config
from filtering_helper import dataframe_check

def filter_files(nutrition_subgroup : str = None, food_type : str = None, description : str = None, weight : float = None, 
              unit : str = None, ingredients : list = None, project_name : str = None, rgbd_file_names : list = None, 
              nutrition_facts_sources : list = None, texture_sources : list = None, quality : int = None, quality_comments : str = None,
              merged : bool = None, textured : bool = None, started : str = None, ended : str = None) -> list[str]:
    
    """Filters the dataframes based on the given parameters
    
    Args:
        nutrition_subgroup (str, optional): The nutrition subgroup. Defaults to None.
        food_type (str, optional): The food type. Defaults to None.
        description (str, optional): The description. Defaults to None.
        weight (float, optional): The weight. Defaults to None.
        unit (str, optional): The unit. Defaults to None.
        ingredients (list, optional): The ingredients. Defaults to None.
        project_name (str, optional): The project name. Defaults to None.
        rgbd_file_names (list, optional): The rgbd file names. Defaults to None.
        nutrition_facts_sources (list, optional): The nutrition facts sources. Defaults to None.
        texture_sources (list, optional): The texture sources. Defaults to None.
        quality (int, optional): The quality. Defaults to None.
        quality_comments (str, optional): The quality comments. Defaults to None.
        merged (bool, optional): The merged. Defaults to None.
        textured (bool, optional): The textured. Defaults to None.
        started (str, optional): The started. Defaults to None.
        ended (str, optional): The ended. Defaults to None.
    Return:
        list[str]: The list of satisfied files
    """

    data_dir_path = Path(__file__).parent.parent / "sample toml files"
    config = Config(data_dir_path, "toml")
    df_list = run(config)

    satisfied_files = []

    for df in df_list:
        gid = df.loc["nutrition_subgroup", "gid"]
        if dataframe_check(df, nutrition_subgroup, food_type, description, weight, unit, ingredients, project_name, rgbd_file_names, 
                        nutrition_facts_sources, texture_sources, quality, quality_comments, merged, textured, started, ended):
            satisfied_files.append(gid)
        
    print(satisfied_files)
    return satisfied_files


if __name__ == "__main__":
    filter_files("pancakes waffles french toast")