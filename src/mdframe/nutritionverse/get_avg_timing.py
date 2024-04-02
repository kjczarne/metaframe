import argparse
import pandas as pd
from pathlib import Path
from rich.console import Console
from mdframe.reader import Config, run, SUPPORTED_METADATA_FILE_EXTENSIONS
from mdframe.timing import calc_time_and_rate_from_a_generic_df


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory',
                        help='Path to the directory containing metadata files',
                        default='test/data_dir')
    parser.add_argument('-m', '--metadata-ext',
                        choices=SUPPORTED_METADATA_FILE_EXTENSIONS,
                        default='toml')
    parser.add_argument('-s', '--schema',
                        help='URL or Path to the schema file for validating the metadata',
                        default=Path(__file__).parent.parent / "schema.json")
    args = parser.parse_args()
    console = Console()

    config = Config(
        data_dir_path=Path(args.directory),
        metadata_file_extension=args.metadata_ext,
        schema_url=Path(args.schema)
    )
    dfs = run(config)
    total_time, rate = calc_time_and_rate_from_a_generic_df(dfs, start_key="started", end_key="finished")
    console.print(f"[blue]Total time invested: {total_time}[/blue]")
    console.print(f"[blue]Rate: {rate}[/blue]")


if __name__ == "__main__":
    main()
