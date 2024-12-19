# geoloc-util

Geolocation utility using Open Weather Geocoding API

## Prerequisites
1. Python 3 is installed
2. `pip` tool is installed for Python
3. Docker is installed


## Installation

1. Clone this repository using `git clone` command
2. (Optional but recommended) Create a Python virtual environment on your system using your preferred tool. For example:
```bash
python3 -m venv Geo
```
which will create a Geo virtual environment in the directory where you are located. You might want to choose a dedicated directory or your virtual environments.

3. Activate the virtual environment using:
```bash
source <path-to-activate binary>
```
on Linux/MacOs. If you are in the same directory as the "Geo" venv from the example above, your command will look like this:
```bash
source Geo/bin/activate
```
On Windows, you may be restricted from launching scripts by PowerShell. To enable external script execution for Windows, change the ExecutionPolicy like this:
```bash
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```
once that's done, navigate to `Geo\Scripts\` directory and activate your virtual environment:
```bash
./activate
```
`Geo` should appear before the Terminal/PowerShell prompt.

4. Install project dependencies by navigating to the project root folder and running this command:
```bash
pip install -r requirements.txt
```




## Usage
1. The `geoloc.py` command-line utility has 3 arguments: `-l` (locations) `-apikey` and `-v` (verbose). Please examine `geoloc.py` file for  its `argparse` setup. Locations and apikey are required.

2. `geoloc.py` sample commands. The arguments is a space-separate list of quoted strings, with any number of items:

```bash
python3 geoloc.py  -l "Los Angeles, CA" -apikey "apikeystring"
python3 geoloc.py -l "60091" -apikey "apikeystring"
python3 geoloc.py -l "60091" "Los Angeles, CA" "Chicago, IL" -apikey "apikeystring" -v
```

## Testing

1. Tests reside in the `/tests` directory of the project. 

2. There are 3 sets of tests, `tests_direct.py` (calls real APIs by using one of the core functions of the `geoloc.py`, `tests_with_subprocess.py` which invokes `geoloc.py` via `subprocess` module (this is the closest to calling it directly via command-line), and `tests_mocked.py`, which is a mocked version of the tests.

3. This project is using Pytest to execute test suites, as follows:

```bash
pytest tests/test_name.py
```
3. You may also use Docker to build a docker image from the `Dockerfile` provided and run tests using Docker engine:

4. Via the CircleCI pipeline as indicated below in CI Integration.

```bash
docker build -t geoloc-tests .
docker run geoloc-tests pytest tests/tests_name.py 
```
## CI Integration

This project is integrated into a `CircleCI` pipeline, with tests running as a PR check, automatically upon branch commits (see `View Details` of any existing PR). You may run tests by simply going to the CircleCI progect `geoloc-util` via `View Details` links provided by GitHub, selecting `main` branch and clicking `Trigger Pipeline` button at the top right corner. The results will appear in the `STEPS` tab of the run, `Run Tests` stage.

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
