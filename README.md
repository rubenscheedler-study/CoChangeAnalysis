# CoChangeAnalysis
Analyzes the git structure of a project to find the best configuration of co-change detection.

Also analyzes output from Market Basket Analysis, Dynamic Time Warping and CoCo.

Utilizes smells reported by https://github.com/darius-sas/astracker (ASTracker)

Related to https://github.com/RonaldKruizinga/CoSmellingChanges (CoCo) 

## Requirements

The requirements to use this script are:
- Python 3.7
- Pip

## Installation

The source code for this project can be cloned using Git or downloaded from Github.

The required packages can be installed via the included Pipfile.

## Usage

The analysis can be run in two ways. The first is by running ```Main.py```. This file has a few different methods referenced for various purposes.

- ```hyper_param_analysis()``` and ```threshold_distribution()``` are used to generate hyperparameters for CoCo. ```threshold_distribution()``` requires CoCo to have run with a threshold of 1 first, so that it can calculate the distribution.

- ```generate_analysis()``` is used to run the market basket analysis and dynamic time warping

- ```run_exploration()``` runs a data exploration on all three algorithm, also using the output from ASTracker. For large projects, this should be done on a server cluster with a significant amount of memory. Example scripts for this can be found in the ```execution_scripts``` folder. These examples are used to run the project on the Peregrine Cluster of the University of Groningen.

- ```results_analysis()``` analyses the results and provides some interesting plots.


## Configuration

In order to use the application to analyse hyperparameters for a project, certain properties in the config.py, located in the main directory, need to be set.

An example is left in the config for the Sonarlint-IntelliJ project.

- A ```github api key``` is required in order to recover the dates of analyzed commits
- A ```start and end date``` of the analysis are required as a time range.
- Project information, such as ```name, url, branch and owner``` are required
- Directories, such as ```input, output and cloning``` directories can be configured

## Input

As input the application can require the output from CoCo and ASTracker.

## Output

The system outputs the co-changes detected using the MBA and DTW algorithms, as well as statistics regarding the overlap of smells with co-changes.

## Structure

- ```helper_scripts``` provide utility functions
- ```hyperparameter_analysis``` provides all necessary functions for that purpose
- ```model``` contains the classes defined
- ```results_analysis``` contains code for plotting interesting plots.

