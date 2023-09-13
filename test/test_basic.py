import pytest
from pathlib import Path
from metaframe import run, Config


def test_metadata_print():
    data_dir_path = Path(__file__).parent / "data_dir"
    config = Config(data_dir_path, "toml", ["txt"])
    df = run(config)
    print(df)


if __name__ == "__main__":
    pytest.main()
