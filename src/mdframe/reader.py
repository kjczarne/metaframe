import argparse
import pandas as pd
import toml
from typing import Dict, Any, Tuple, Optional, Literal, get_args, List
from pathlib import Path
from dataclasses import dataclass

DataFileExtension = Literal["txt", "jpg"]
SUPPORTED_DATA_FILE_EXTENSIONS = get_args(DataFileExtension)

MetadataFileExtension = Literal["toml"]
SUPPORTED_METADATA_FILE_EXTENSIONS = get_args(MetadataFileExtension)


def load_metadata_file(metadata_file_path: Path) -> Dict[str, Any]:
    if not metadata_file_path.exists():
        raise ValueError(f"Path {metadata_file_path} does not seem to point to a valid file")

    with open(metadata_file_path, "r") as f:
        metadata_file_contents = toml.load(f)

    return metadata_file_contents


def metadata_file_to_df(metadata_file_contents):
    return pd.DataFrame(metadata_file_contents)


def data_dir_to_dataframes(data_dir_path: Path, metadata_file_extension: MetadataFileExtension) -> List[pd.DataFrame]:
    metadata_file_paths = data_dir_path.glob(f"*.{metadata_file_extension}")
    metadata_file_contents = map(load_metadata_file, metadata_file_paths)
    metadata_records = map(metadata_file_to_df, metadata_file_contents)
    return list(metadata_records)


@dataclass
class Config:
    data_dir_path: Path
    metadata_file_extension: Optional[MetadataFileExtension]
    # data_file_extensions: List[DataFileExtension]


def run(config: Config):
    return data_dir_to_dataframes(**config.__dict__)


def main():
    parser = argparse.ArgumentParser('mdframe', 'Prints metadatafiles in a neat dataframe')
    parser.add_argument('-d', '--directory',
                        type=str,
                        help="Path to the directory containing the data and the metadata",
                        default="data")
    parser.add_argument('-m', '--metadata-ext',
                        help="Extension of the metadata files",
                        choices=SUPPORTED_METADATA_FILE_EXTENSIONS,
                        default="toml")
    args = parser.parse_args()
    config = Config(
        Path(args.directory),
        args.metadata_ext,
    )
    dfs = run(config)
    print(dfs)


if __name__ == "__main__":
    main()
