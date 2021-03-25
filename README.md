# Project name

[![Zenodo badge](https://zenodo.org/badge/doi/___doi1___.svg)](https://doi.org/___doi1___)
[![PEP compatible](http://pepkit.github.io/img/PEP-compatible-green.svg)](http://pep.databio.org/)

[![medRxiv badge](https://zenodo.org/badge/doi/__doi1___.svg)](https://doi.org/__doi1___) ⬅️ read the preprint here

Project description

## Organization

- The [metadata](metadata) directory contains metadata relevant to annotate the samples
- [This CSV file](metadata/samples.csv) is the master record of all analyzed samples
- The [src](src) directory contains source code used to analyze the data
- Raw data (i.e. MCD files) will be under the `data` directory.
- Processing of the data will create TIFF files under the `processed`  directory.
- Outputs from the analysis will be present in a `results` directory, with subfolders pertaining to each part of the analysis as described below.


Raw data in the form of ___X___ are hosted on WCM's enterprise version of Box.com. An account is needed to download the files, which can be made programmatically with the [imctransfer](https://github.com/ElementoLab/imctransfer) program.
For now you'll need a developer token to connect to box.com programmatically. Place the credentials in a JSON file in `~/.imctransfer.auth.json`. Be sure to make the file read-only (e.g. `chmod 400 ~/.imctransfer.auth.json`).

## Reproducibility

### Running

To see all available steps type:
```bash
$ make
```

Steps used for the initiall processing of raw data are marked with the `[dev]` label.
```
Makefile for the covid-imc project/package.
Available commands:
help                Display help and quit
requirements        Install Python requirements
transfer            [dev] Transfer data from wcm.box.com to local environment
process             [dev] Process raw data into processed data types
sync                [dev] Sync data/code to SCU server
upload_data         [dev] Upload processed files to Zenodo
download_data       Download processed data from Zenodo (for reproducibility)
analysis            Run the actual analysis
```

To reproduce analysis using the pre-preocessed data, one would so:

```bash
$ make help
$ make requirements   # install python requirements using pip
$ make download_data  # download processed from Zenodo
$ make analysis       # run the analysis scripts
```

#### Requirements

- Python 3.7+ (was run on 3.8.2)
- Python packages as specified in the [requirements file](requirements.txt) - install with `make requirements` or `pip install -r requirements.txt`.

Feel free to use some virtualization or compartimentalization software such as virtual environments or conda to install the requirements.

#### Virtual environment

It is recommended to compartimentalize the analysis software from the system's using virtual environments, for example.

Here's how to create one with the repository and installed requirements:

```bash
git clone git@github.com:___gituser/repo___.git
cd covid-imc
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
