import argparse
import json
import warlock
from warlock.core import model as warlock_model
from dataclasses import dataclass, field
from jsonschema import validate, ValidationError, SchemaError
import pandas as pd
import toml
from toml.decoder import TomlDecodeError
from typing import Dict, Any, Tuple, Optional, Literal, get_args, List, Iterator, Callable, Type
from pathlib import Path
from toolz import compose_left
from functools import partial
import urllib3
from urllib.parse import urlparse
from urllib3.exceptions import HTTPError


DataFileExtension = Literal[".txt", ".jpg"]
MetadataFileExtension = Literal[".toml"]
DataframeBackend = Literal["pandas", "polars", "raw"]

SUPPORTED_DATA_FILE_EXTENSIONS = get_args(DataFileExtension)
SUPPORTED_METADATA_FILE_EXTENSIONS = get_args(MetadataFileExtension)
SUPPORTED_DATAFRAME_BACKENDS = get_args(DataframeBackend)


class DynClass(warlock_model.Model):
    """A class that corresponds to a Warlock-generated class.
    It makes no assumptions on the class members or methods and
    serves purely for data representation.
    """


@dataclass
class Config:
    metadata_file_paths: List[Path] | Path
    metadata_file_extension: MetadataFileExtension | None
    schema_loc: Path
    representation: DataframeBackend = "raw"
    sort: bool = True
    __schema: Dict | None = field(default=None, repr=False)  # avoiding nasty prints
    __class_: Any | None = field(default=None, repr=False)

    @property
    def schema(self):
        """Loads the schema from the schema location and returns it as a dictionary."""
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

    @property
    def Class(self) -> Type[DynClass]:
        """Generates a Warlock class based on the schema and returns it."""
        if self.__class_ is None:
            self.__class_ = warlock.model_factory(self.schema)
        return self.__class_


    def _load_one_metadata_file(self, metadata_file_path: Path) -> DynClass:
        """Loads a single metadata file and returns its contents as a Warlock object."""
        filename_suffix = metadata_file_path.suffix
        if filename_suffix not in SUPPORTED_METADATA_FILE_EXTENSIONS:
            raise ValueError(f"Crashed when processing metadata file. {filename_suffix} is not supported")

        if not metadata_file_path.exists():
            raise FileNotFoundError(f"Path {metadata_file_path} does not seem to point to a valid file")

        specific_file_name = metadata_file_path.name

        try:
            with open(metadata_file_path, "r") as f:
                metadata_file_contents = toml.load(f)
        except toml.decoder.TomlDecodeError as toml_error:
            raise TomlDecodeError(f"Crashed when processing metadata file {specific_file_name}; {toml_error}", doc=toml_error.doc, pos=toml_error.pos) from toml_error

        return self.Class(metadata_file_contents)  # pylint: disable=not-callable


def glob_all_dirs(path: Path | List[Path], pattern: str) -> Iterator[Path]:
    if isinstance(path, list):
        for p in path:
            yield from glob_all_dirs(p, pattern)
        return
    if path.is_dir():
        yield from path.glob(pattern)
        


def load_metadata_files(config: Config,
                        transform_fn: Callable[[DynClass], Any] = lambda x: x) -> Iterator[DynClass | Any]:

    globbed_metadata_file_paths = glob_all_dirs(config.metadata_file_paths,
                                                f"*.{config.metadata_file_extension}")

    # Optionally sort the paths:
    if config.sort:
        output_metadata_file_paths = sorted(globbed_metadata_file_paths)
    else:
        output_metadata_file_paths = globbed_metadata_file_paths

    # Define a sequence of functions to apply to each path left-to-right:
    f = compose_left(config._load_one_metadata_file,
                     transform_fn)
    # Note that after `transform_fn` is applied a `DynClass` instance
    # can be transformed into any arbitrary object, hence `Any`.

    # Use a generator to yield files one-by-one in a lazy fashion:
    yield from (f(path) for path in output_metadata_file_paths)


def metadata_file_to_pandas_df(metadata_file_contents: DynClass) -> pd.DataFrame:
    return pd.DataFrame(dict(metadata_file_contents))


def run(config: Config, lazy: bool = True) -> Iterator[Any]:
    if lazy:
        # If lazy, we want to return a generator:
        load_fn = partial(load_metadata_files, config=config)
    else:
        # If not lazy, we want to load all metadata files at once
        # and return a list of them:
        load_fn = compose_left(partial(load_metadata_files, config=config),
                               list)

    # Then we match on the representation switch to decide which backend to use:
    match config.representation:
        case "pandas":
            return load_fn(transform_fn=metadata_file_to_pandas_df)
        case "polars":
            raise NotImplementedError("Polars backend is not yet implemented")
        case "raw":
            return load_fn()  # relying on the identity lambda from `load_metadata_files`
        case _:
            raise ValueError(f"Unsupported representation {config.representation}")


def run_eager(config: Config) -> List[Any]:
    """Alias for `run(config, lazy=False)`"""
    return run(config, lazy=False)


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
                        default=Path(__file__).parent / "data")
    parser.add_argument('-m', '--metadata-ext',
                        help="Extension of the metadata files",
                        choices=SUPPORTED_METADATA_FILE_EXTENSIONS,
                        default="toml")
    parser.add_argument('-s', '--schema',
                        type=str,
                        help="URL or Path to the schema file for validating the metadata",
                        default=Path(__file__).parent / "schema.json")
    parser.add_argument('--sort',
                        action='store_true',
                        help="Sort the metadata files in ascending filename order before parsing")
    parser.add_argument('-r', '--representation',
                        choices=SUPPORTED_DATAFRAME_BACKENDS,
                        help="Choose the backend for the dataframe representation",
                        default="raw")
    args = parser.parse_args()

    schema = args.schema
    if args.schema != Path(__file__).parent / "schema.json":
        schema = get_appropriate_schema(args.schema)

    config = Config(
        metadata_file_paths=Path(args.directory),
        metadata_file_extension=args.metadata_ext,
        schema_loc=schema,
        representation=args.representation,
        sort=args.sort
    )
    dfs = list(run(config, lazy=False))
    print(dfs)
    print("Done")


if __name__ == "__main__":
    main()

