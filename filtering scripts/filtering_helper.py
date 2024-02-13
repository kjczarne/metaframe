def check_equality(category : str, df_category : str) -> bool:
    """Checks if the category is the same as the one in the dataframe
    
    Args:
        category (str): The category
        df_category (str): The category in the dataframe
    
    Returns:
        bool: True if the category is the same as the one in the dataframe or None, False otherwise
    """
    if category == None:
        return True
    return category == df_category

def check_category_existence(category : str, df : str) -> bool:
    """Checks if the category exists in the dataframe index
    
    Args:
        category (str): The category
        df (pandas.DataFrame): The category in the dataframe
    
    Returns:
        bool: True if the category exists in the dataframe index, False otherwise
    """
    if category in list(df.index):
        return True
    
    return False

def dataframe_check(df, nutrition_subgroup : str = None, food_type : str = None, description : str = None, weight : float = None,
                     unit : str = None, ingredients : list = None, project_name : str = None, rgbd_file_names : list = None,
              nutrition_facts_sources : list = None, texture_sources : list = None, quality : int = None, quality_comments : str = None,
              merged : bool = None, textured : bool = None, started : str = None, ended : str = None) -> bool:
    
    """Filters the dataframe based on the given parameters
    
    Args:
        df (pd.DataFrame): The dataframe
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
        bool: True if the dataframe satisfies the given parameters, False otherwise
    """

    categories_list = ["nutrition_subgroup", "food_type", "description", "weight", "unit", "ingredients", "project_name", "rgbd_file_names", 
                       "nutrition_facts_sources", "texture_sources", "quality", "quality_comments", "merged", "textured", "started", "finished"]
    
    categories_item = ["nutrition_subgroup", "food_type", "description"]
    categories_metrics = ["weight", "unit", "ingredients"]
    categories_model = ["project_name", "rgbd_file_names", "nutrition_facts_sources", "texture_sources", "quality", "quality_comments", "merged", "textured"]
    categories_time = ["started", "finished"]

    categories_existence = []

    for category in categories_list:
        if not check_category_existence(category, df):
            categories_existence.append(None)
            continue
        
        if category in categories_item:
            categories_existence.append(df.loc[category, "item"])
        elif category in categories_metrics:  
            categories_existence.append(df.loc[category, "metrics"])
        elif category in categories_model:
            categories_existence.append(df.loc[category, "model"])
        elif category in categories_time:
            categories_existence.append(df.loc[category, "time"])

    argument_list = [nutrition_subgroup, food_type, description, weight, unit, ingredients, project_name, 
                     rgbd_file_names, nutrition_facts_sources, texture_sources, quality, quality_comments, merged, textured, started, ended]
    
    for index in range(len(argument_list)):
        if not check_equality(argument_list[index], categories_existence[index]):
            return False
    return True
