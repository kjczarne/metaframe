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


def load_file_pair(metadata_file_path: Path,
                   data_file_path: Path) -> Tuple[Dict[str, Any], None]:
    if not metadata_file_path.exists():
        raise ValueError(f"Path {metadata_file_path} does not seem to point to a valid file")

    with open(metadata_file_path, "r") as f:
        metadata_file_contents = toml.load(f)

    # with open(data_file_path, "r") as f:
    # TODO: load metadata from different file types and put them into separate columns of the dataframe
    return metadata_file_contents, None


def file_pair_to_record(metadata_file_contents, data_file_contents):
    return pd.Series(metadata_file_contents)


def data_directory_to_dataframe(data_dir_path: Path,
                                metadata_file_extension: Optional[MetadataFileExtension],
                                data_file_extensions: List[DataFileExtension]):
    list_of_all_datafiles = []
    for ext in data_file_extensions:
        glob_pattern_datafile = "*." + ext
        list_of_all_datafiles.extend(data_dir_path.glob(glob_pattern_datafile))

    list_of_records = []
    for file_path in list_of_all_datafiles:
        file_name_stem = file_path.stem  # `stem` gets the filename without the extension
        if metadata_file_extension is not None:
            file_pair = load_file_pair(file_path.parent / (file_name_stem + "." + metadata_file_extension), file_path)
        else:
            file_pair = load_file_pair(file_path.parent / file_name_stem, file_path)
        series = file_pair_to_record(*file_pair)
        list_of_records.append(series)
    return pd.DataFrame(list_of_records)


@dataclass
class Config:
    data_dir_path: Path
    metadata_file_extension: Optional[MetadataFileExtension]
    data_file_extensions: List[DataFileExtension]


def run(config: Config):
    return data_directory_to_dataframe(**config.__dict__)


def main():
    parser = argparse.ArgumentParser('mdframe', 'Prints metadatafiles in a neat dataframe')
    parser.add_argument('-d', '--directory',
                        type=str,
                        help="Path to the directory containing the data and the metadata")
    parser.add_argument('-e', '--ext',
                        type=str,
                        help="Extension of the data files",
                        choices=SUPPORTED_DATA_FILE_EXTENSIONS,
                        nargs="+")
    parser.add_argument('-m', '--metadata-ext',
                        help="Extension of the metadata files",
                        choices=SUPPORTED_METADATA_FILE_EXTENSIONS)
    args = parser.parse_args()
    config = Config(
        Path(args.directory),
        args.metadata_ext,
        args.ext
    )
    print(run(config))


if __name__ == "__main__":
    main()
