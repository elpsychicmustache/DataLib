# DataLib

DataLib is a Python library for performing a standardized method of data exploration on datasets. It builds off of Pandas, providing ease-of-use suites of commonly used functions and data exploration methods for data cleaning, transformation, and visualization. Currently, this code is based off the teachings of Rob Mulla https://www.youtube.com/watch?v=xi0vhXFPegw, but I plan to bring in concepts from other creators and mentors.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)

## Installation

Currently, you will need to install the code directly from Github and save the code as a local package called datalib.

Additionally, you need to have pandas installed.

## Usage

Here is an example of how to use DataLib:

import datalib as dlm

# Load the data into a dataframe.
data_manager = dlm.DataframeManager("data.csv")

# Get general information about the dataframe.
data_manager.understand_data()

# Do some general data processing to prepare data for analysis.
data_manager.prepare_data()