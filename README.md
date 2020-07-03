# CoChangeAnalysis
Analyzes the git structure of a project to find the best configuration of co-change detection.

Related to https://github.com/RonaldKruizinga/CoSmellingChanges

## Requirements

The requirements to use this script are:
- Python 3.7
- Pip

## Installation

The source code for this project can be cloned using Git or downloaded from Github.

The required packages can be installed via the included Pipfile.

## Usage




## Configuration

In order to use the application to analyse hyperparameters for a project, certain properties in the config.py need to be set.

- A ```github api key``` is required in order to recover the dates of analyzed commits
- A ```start and end date``` of the analysis are required
- Project information, such as ```name, url, branch and owner``` are required
- Directories, such as ```input, output and cloning``` directories can be configured

