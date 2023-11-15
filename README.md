# mdframe

View metadata files as a Pandas DataFrame

## Installation

1. Get [Python Poetry](https://python-poetry.org/)
2. `cd` into the root of this repository
3. Run `poetry install`

## Development

1. For development installation use `poetry install --with dev`.
2. Use `pylint` as the linter. Configuration for `pylint` is provided in `pyproject.toml`.
3. Use `unittest` to develop and run unit- and integration tests (`pytest` is a nightmare to debug in VSCode).
4. If you're adding new functionality, please write a test for it and make sure all tests are passing before submitting a pull request.
5. Keep commit messages informative. It is unacceptable to use dummy commit messages.
6. Keep commits small and commit often.
7. Document your functions using Google docstring style. Use typing annotations at the very least in function/method signatures.

> 👀 It's recommended to use VSCode debugger for development. Configurations for the debugger are provided under `.vscode/launch.json`.
