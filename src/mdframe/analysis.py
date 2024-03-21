from pathlib import Path
from typing import Dict, Any, Tuple, Optional, Literal, get_args, List
from reader import Config, run
import pandas as pd
import matplotlib.pyplot as plt

config = Config(
    data_dir_path=Path(__file__).parent / "data_dir", 
    metadata_file_extension="toml",
    schema_loc=Path('schema.json')
)

def load_flattened_data(config):
    def flatten_property_dict(property_dict: Dict) -> Dict:
        flattened_dict = dict()
        for property_name, value in property_dict.items():
            if isinstance(value, dict):
                for subproperty, subvalue in value.items():
                    flattened_dict[subproperty] = subvalue
            else:
                flattened_dict[property_name] = value
        return flattened_dict

    entries = run(config)
    
    # convert all pandas Series objects into dictionaries, and flatten them in order to isolate property_name
    entries = [pd.Series.to_dict(entry) for entry in entries]
    entries = [flatten_property_dict(entry) for entry in entries]

    df = pd.DataFrame(entries)
    return df

def filter_data(config, query, filename):
    df = load_flattened_data(config)

    # df.query has many limitations, so ditching that for eval(query)
    # df = df.query(query)

    df = df[eval(query)]
    print(df)

    df.to_csv(filename)
  
# TODO: augment generate_histogram to use load_data function
def generate_histogram(config, property_name='quality', data_type='discrete'):
    """Generates a histogram based on the given configuration, property name, and data type.

    Args:
        config: The configuration for generating the histogram.
        property_name (str, optional): The name of the property. Defaults to 'quality'.
        data_type (str, optional): The type of data. Either 'discrete' or 'continuous'. Defaults to 'discrete'.

    Raises:
        ValueError: If the data type is not 'discrete' or 'continuous'.

    Returns:
        None
    """

    def flatten_property_dict(property_dict: Dict) -> Dict:
        flattened_dict = dict()
        for property_name, value in property_dict.items():
            if isinstance(value, dict):
                for subproperty, subvalue in value.items():
                    flattened_dict[subproperty] = subvalue
            else:
                flattened_dict[property_name] = value
        return flattened_dict

    if data_type not in ['discrete', 'continuous']:
        raise ValueError(f"{data_type} must either be 'discrete' or 'continuous'")

    entries = run(config)
    
    # convert all pandas Series objects into dictionaries, and flatten them in order to isolate property_name
    entries = [pd.Series.to_dict(entry) for entry in entries]
    entries = [flatten_property_dict(entry) for entry in entries]

    # extract all model quality data and generate a model histogram
    property_data = []

    for entry in entries:
        if property_name in entry:
            property_data.append(entry[property_name])
    
    if len(property_data) == 0:
        raise ValueError(f'No entries with column name {property_name} found')

    # property_series = pd.Series(property_data)
    # property_series.plot.hist()

    if data_type == 'discrete':
        unique_values = sorted(set(property_data))
        frequencies = [property_data.count(value) for value in unique_values]

        plt.xticks(unique_values)
        plt.bar(unique_values, frequencies, align='center')  
    else:
        plt.hist(property_data, bins='auto', edgecolor='black')
        plt.grid(True)

    plt.xlabel('Values')
    plt.ylabel('Frequency')
    plt.title(f'Histogram of {property_name} in Data')

    plt.show()


if __name__ == '__main__':
    df = load_flattened_data(config)
    print(df.columns)

    # generate histogram
    # generate_histogram(config, "quality", data_type='discrete')
    # generate_histogram(config, "weight", data_type='continuous')

    # filter data and get insights
    filter_data(config, "df['quality'] == 1", "quality1-scans.csv")
    filter_data(config, "df['nutrition_facts_sources'].astype(bool)", "empty-nutrition-facts.csv")
