import argparse
import json
from dataclasses import dataclass
from jsonschema import validate, ValidationError, SchemaError
import pandas as pd
import toml
from toml.decoder import TomlDecodeError
from typing import Dict, Any, Tuple, Optional, Literal, get_args, List
from pathlib import Path
import urllib3
from urllib.parse import urlparse
from urllib3.exceptions import HTTPError

DataFileExtension = Literal["txt", "jpg"]
SUPPORTED_DATA_FILE_EXTENSIONS = get_args(DataFileExtension)

MetadataFileExtension = Literal["toml"]
SUPPORTED_METADATA_FILE_EXTENSIONS = get_args(MetadataFileExtension)

@dataclass
class Config:
    data_dir_path: Path
    metadata_file_extension: Optional[MetadataFileExtension]
    # data_file_extensions: List[DataFileExtension]
    schema_loc: Path | str
    __schema: Dict | None = None

    @property
    def schema(self):
        if self.__schema is None:
            if isinstance(self.schema_loc, Path):
                if not self.schema_loc.exists():
                    raise ValueError(f"Path {self.schema_loc} does not seem to point to a valid JSON schema file")

                with open(self.schema_loc, "r") as f:
                    self.__schema = json.loads(f.read())
            elif urlparse(self.schema_loc).scheme in ['http', 'https']: # schema_url is a string (representing a URL)
                http = urllib3.PoolManager()
                response = http.request('GET', self.schema_loc)

                if response.status == 200:
                   self.__schema = json.loads(response.data.decode('utf-8'))
                else:
                    raise HTTPError(f"Failed to fetch schema from URL {self.schema_loc}")
            else:
                raise ValueError(f"Passed schema location is not a path or a URL")
        return self.__schema

def load_metadata_file(metadata_file_path: Path, schema: Dict) -> Dict[str, Any]:
    # starting this indexing at 1 to shave off the '.' to get the actual extension
    filename_suffix = metadata_file_path.suffix[1:]
    if filename_suffix not in SUPPORTED_METADATA_FILE_EXTENSIONS:
        raise ValueError(f"Crashed when processing metadata file {specific_file_name}; {filename_suffix} is not supported")

    if not metadata_file_path.exists():
        raise FileNotFoundError(f"Path {metadata_file_path} does not seem to point to a valid file")

    try:
        with open(metadata_file_path, "r") as f:
            metadata_file_contents = toml.load(f)
    except toml.decoder.TomlDecodeError as toml_error:
        specific_file_name = str(metadata_file_path)
        specific_file_name = specific_file_name[specific_file_name.rfind('/')+1:]

        raise TomlDecodeError(f"Crashed when processing metadata file {specific_file_name}; {toml_error}", doc=toml_error.doc, pos=toml_error.pos) from toml_error

    try:
        # validates JSON according to schema located in schema.json
        validate(instance = metadata_file_contents, schema = schema)
    except SchemaError as schema_error:
        specific_file_name = str(metadata_file_path)
        specific_file_name = specific_file_name[specific_file_name.rfind('/')+1:]
        raise SchemaError(f"Crashed when processing metadata file {specific_file_name}; {schema_error.message}") from schema_error
    except ValidationError as validation_error:
        specific_file_name = str(metadata_file_path)
        specific_file_name = specific_file_name[specific_file_name.rfind('/')+1:]
        raise ValidationError( f"Crashed when processing metadata file {specific_file_name}; {validation_error.message}") from validation_error

    return metadata_file_contents


def metadata_file_to_df(metadata_file_contents):
    return pd.DataFrame(metadata_file_contents)


def data_dir_to_dataframes(data_dir_path: Path,
                           metadata_file_extension: MetadataFileExtension,
                           schema: Dict) -> List[pd.DataFrame]:
    metadata_file_paths = data_dir_path.glob(f"*.{metadata_file_extension}")    
    metadata_file_contents = [load_metadata_file(path, schema) for path in metadata_file_paths]
    
    metadata_records = []
    for text in metadata_file_contents:
        metadata_records.append(pd.Series(text))

    return metadata_records
    
@dataclass
class Config:
    data_dir_path: Path
    metadata_file_extension: Optional[MetadataFileExtension]
    # data_file_extensions: List[DataFileExtension]
    schema_loc: Path | str
    __schema: Dict | None = None

    @property
    def schema(self):
        if self.__schema is None:
            if isinstance(self.schema_loc, Path):
                if not self.schema_loc.exists():
                    raise ValueError(f"Path {self.schema_loc} does not seem to point to a valid JSON schema file")

                with open(self.schema_loc, "r") as f:
                    self.__schema = json.loads(f.read())
            elif isinstance(self.schema_loc, str): # schema_url is a string (representing a URL)
                http = urllib3.PoolManager()
                response = http.request('GET', self.schema_loc)

                if response.status == 200:
                   self.__schema = json.loads(response.data.decode('utf-8'))
                else:
                    raise HTTPError(f"Failed to fetch schema from URL {self.schema_loc}")
            else:
                raise ValueError(f"Specified schema location {self.schema_loc} is neither a URL nor Path")
        return self.__schema


def run(config: Config):
    return data_dir_to_dataframes(
        data_dir_path=config.data_dir_path, 
        metadata_file_extension=config.metadata_file_extension, 
        schema=config.schema
    )

def get_appropriate_schema(schema_data: str):
    # parse schema url to determine whether Url or Path passed
    parsed_schema = urlparse(schema_data)

    if len(parsed_schema.scheme) == 0 or (parsed_schema.scheme not in ['http', 'https']):
        return schema_data
    elif Path(schema_data).exists():
        return Path(schema_data)

    raise ValueError(f"Specified schema location {parsed_schema} is neither a URL nor Path")


def main():
    parser = argparse.ArgumentParser('mdframe', 'Prints metadatafiles in a neat dataframe')
    parser.add_argument('-d', '--directory',
                        type=str,
                        help="Path to the directory containing the data and the metadata",
                        default=Path(__file__).parent / "data_dir")
    parser.add_argument('-m', '--metadata-ext',
                        help="Extension of the metadata files",
                        choices=SUPPORTED_METADATA_FILE_EXTENSIONS,
                        default="toml")
    parser.add_argument('-s', '--schema',
                        type=str,
                        help="URL or Path to the schema file for validating the metadata",
                        default=Path(__file__).parent / "schema.json")
    args = parser.parse_args()

    schema = args.schema
    if args.schema != Path(__file__).parent / "schema.json":
        schema = get_appropriate_schema(args.schema)
    
    config = Config(
        data_dir_path=Path(args.directory),
        metadata_file_extension=args.metadata_ext,
        schema_loc=schema,
    )
    dfs = run(config)
    print(dfs)


if __name__ == "__main__":
    main()
