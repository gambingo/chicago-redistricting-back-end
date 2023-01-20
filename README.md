# Chicago Redistricting – Back End

TKTK

### Data
- [Boundaries - City](https://data.cityofchicago.org/Facilities-Geographic-Boundaries/Boundaries-City/ewy2-6yfk)
- [Boundaries - Community Areas (current)](https://data.cityofchicago.org/Facilities-Geographic-Boundaries/Boundaries-Community-Areas-current-/cauq-8yn6)
- [Boundaries - Neighborhoods](https://data.cityofchicago.org/Facilities-Geographic-Boundaries/Boundaries-Neighborhoods/bbvz-uum9)
- [Boundaries - Wards (2003-2015)](https://data.cityofchicago.org/Facilities-Geographic-Boundaries/Boundaries-Wards-2003-2015-/xt4z-bnwh)
- [Boundaries - Wards (2015-2023)](https://data.cityofchicago.org/Facilities-Geographic-Boundaries/Boundaries-Wards-2015-2023-/sp34-6z76)
- [Boundaries - Wards (2023-)](https://data.cityofchicago.org/Facilities-Geographic-Boundaries/Boundaries-Wards-2023-/p293-wvbd)
- [2020 Decennial Redistricting Data (i.e. "the census") for all census blocks in Cook County](https://data.census.gov/table?g=0500000US17031$1000000&y=2020&d=DEC+Redistricting+Data+(PL+94-171)&tid=DECENNIALPL2020.P1)
- [Census Bureau TIGER/Line® Shapefiles](https://www.census.gov/cgi-bin/geo/shapefiles/index.php)
    - [2020 TIGER/Line® Shapefiles: Census Tracts](https://www.census.gov/cgi-bin/geo/shapefiles/index.php?year=2020&layergroup=Census+Tracts)
<br>


### References
- [Dual Annealing Optimization With Python](https://machinelearningmastery.com/dual-annealing-optimization-with-python) by Jason Brownlee
<br>


### Development

1. This project was built with Python version `3.10.9`. I use [Pyenv](https://github.com/pyenv/pyenv#installation) to manage my Python installation.

1. This project uses [Poetry](https://python-poetry.org/docs/master/#installation) to manage dependencies. Install e'rything with:
    ```bash
    poetry install
    ```

1. If you would like to work with jupyter notebooks while using Poetry, run:
    ```bash
    poetry run python -m ipykernel install --user --name chicago-redistricting
    poetry run jupyter lab
    ```

    Then select the newly created kernel, `chicago-redistricting`, when starting a notebook.


##### Notes on working with Poetry

I had some trouble resolving my installation of Poetry with Pyenv. Poetry seems stuck to the python version from when I installed it and fails to recognize my local python version specified with pyenv. Here is how I have learned to create a new project with Poetry as a workaround.

    ```bash
    mkdir new-project
    cd new-project
    pyenv local 3.10.9
    poetry init

    # Poetry will autocomplete a python version of ^3.9
    # Change this to 3.10.9, or whichever version you prefer
    # Complete project initialization, without interactively specifying dependencies
    poetry env use 3.10.0
    poetry update

    # Now you may specify your depencies like so:
    poetry add package-name
    poetry add dev-package1 dev-package2 --group dev
    ```