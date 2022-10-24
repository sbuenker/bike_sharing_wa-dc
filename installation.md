## Requirements and Installation

### Requirements
* pyenv with Python: 3.9.8

### Installation 

1. First clone the repository using:
 ```Bash
 git clone git@github.com:sbuenker/bike_sharing_wa-dc.git
 ```
2. Navigate to the repository using:
 ```Bash
 cd bike_sharing_wa-dc
 ```
3. For installing the virtual environment you can either use the Makefile and run `make setup` or install it manually with the following commands: 
```Bash
 pyenv local 3.9.8
 python -m venv .venv
 source .venv/bin/activate
 pip install --upgrade pip
 pip install -r requirements.txt
```
4. [Optional] Run the Python script [preprocessing_bikes.py](https://github.com/sbuenker/bike_sharing_wa-dc/blob/main/preprocessing_bikes.py) to generate [dc-bikes-daily.csv](https://github.com/sbuenker/bike_sharing_wa-dc/blob/main/data/dc-bikes-daily.csv). To run the script, you first need to navigate to `cd data` and then create a sub-directory `mkdir bike`. The data on bike trips is obtained from the [Capital Bikeshare website](https://s3.amazonaws.com/capitalbikeshare-data/index.html). The data is stored as zip files which need to be downloaded and unzipped to `data/bike`.

5. [Optional] Daily historic weather data for Washington DC is obtained from the [National Oceanic and Atmospheric Administration website](https://www.ncei.noaa.gov/cdo-web/datasets/GHCND/stations/GHCND:USW00013743/detail). The corresponding file is [weather_dc_historic.csv](https://github.com/sbuenker/bike_sharing_wa-dc/blob/main/data/weather_dc_historic.csv).

6. [Optional] Run the Python script [preprocessing_final.py](https://github.com/sbuenker/bike_sharing_wa-dc/blob/main/preprocessing_finaldata.py) to generate the final merged bike and weather data that is used for the analysis. The corresponding file is [finaldata.csv](https://github.com/sbuenker/bike_sharing_wa-dc/blob/main/data/finaldata.csv).

7. The Python script [regressions.py](https://github.com/sbuenker/bike_sharing_wa-dc/blob/main/regressions.py), can be run from the command line. However, to adjust function arguments for the regression test and prediction analysis, this needs to be done directly in the script. 