import argparse
import json
from dataclasses import dataclass
from jsonschema import validate
import pandas as pd
import toml
from typing import Dict, Any, Tuple, Optional, Literal, get_args, List
from pathlib import Path
import urllib3
from urllib3 import Url
from urllib.parse import urlparse
from urllib3.exceptions import HTTPError

DataFileExtension = Literal["txt", "jpg"]
SUPPORTED_DATA_FILE_EXTENSIONS = get_args(DataFileExtension)

MetadataFileExtension = Literal["toml"]
SUPPORTED_METADATA_FILE_EXTENSIONS = get_args(MetadataFileExtension)

def load_metadata_file(metadata_file_path: Path, schema: Dict) -> Dict[str, Any]:
    if not metadata_file_path.exists():
        raise ValueError(f"Path {metadata_file_path} does not seem to point to a valid file")

    with open(metadata_file_path, "r") as f:
        metadata_file_contents = toml.load(f)

    # validates JSON according to schema located in schema.json
    validate(instance = metadata_file_contents, schema = schema)

    return metadata_file_contents


def metadata_file_to_df(metadata_file_contents):
    return pd.DataFrame(metadata_file_contents)


def data_dir_to_dataframes(data_dir_path: Path,
                           metadata_file_extension: MetadataFileExtension,
                           schema: Dict) -> List[pd.DataFrame]:
    metadata_file_paths = data_dir_path.glob(f"*.{metadata_file_extension}")    
    metadata_file_contents = [load_metadata_file(path, schema) for path in metadata_file_paths]
    metadata_records = map(metadata_file_to_df, metadata_file_contents)
    return list(metadata_records)

@dataclass
class Config:
    data_dir_path: Path
    metadata_file_extension: Optional[MetadataFileExtension]
    # data_file_extensions: List[DataFileExtension]
    schema_url: Url | Path
    __schema: Dict | None = None

    @property
    def schema(self):
        if self.__schema is None:
            if isinstance(self.schema_url, Path):
                if not self.schema_url.exists():
                    raise ValueError(f"Path {self.schema_url} does not seem to point to a valid JSON schema file")

                with open(self.schema_url, "r") as f:
                    self.__schema = json.loads(f.read())
            else: # schema_url is of type Url
                http = urllib3.PoolManager()
                response = http.request('GET', self.schema_url)

                if response.status == 200:
                   self.__schema = json.loads(response.data.decode('utf-8'))
                else:
                    raise HTTPError(f"Failed to fetch schema from URL {self.schema_url}")
        return self.__schema

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
    parser.add_argument('-s', '--schema',
                        type=str,
                        help="URL or Path to the schema file for validating the metadata",
                        default="schema.json")
    args = parser.parse_args()

    # parse schema url to determine whether Url or Path passed
    parsed_schema = urlparse(args.schema)
    if parsed_schema.scheme in ['http', 'https']:
        schema = Url(parsed_schema)
    else:
        try:
            Path(args.schema).exists()
            schema = Path(args.schema)
        except:
            raise ValueError(f"Specified schema location {parsed_schema} is neither a URL nor Path")

    config = Config(
        data_dir_path=Path(args.directory),
        metadata_file_extension=args.metadata_ext,
        schema_url=schema,
    )
    dfs = run(config)
    print(dfs)


if __name__ == "__main__":
    main()
