# filewatch
## Table of Contents
* [Overview](#overview)
* [Clone This Repository](#clone-this-repository)
* [Requirements](#requirements)
* [Running The Project](#running-the-project)
* [Files & Directories](#files--directories)

## Overview
Code snippet for a utility that monitors any number of directories and tracks observed file changes. Developed in Python 3.10.12 on Ubuntu (via WSL2).

## Clone This Repository
To clone this repository, with git installed open a terminal and run the following.
```shell
git clone https://github.com/Frosk-Kristian/filewatch.git
```

## Requirements
Used libraries and versions outlined in `requirements.txt`. To install project requirements using pip, open a terminal and navigate to the same directory as `requirements.txt` then run the following.
```shell
pip install -r requirements.txt
```

## Running The Project
To run this project, open a terminal and navigate to the same directory as `main.py` then run the following (subtituting `<path/to/directory>` for the path to the desired directory).
```shell
python3 main.py <path/to/directory>
```

Alternatively, you can monitor multiple directories by supplying additional command line arguments as follows.
```shell
python3 main.py <first_directory> <second_directory> ... <xth_directory>
```

Attempting to run the project without supplying command line arguments will prompt an error message and exit the project early.

## Files & Directories
* [Modules](Modules): Subdirectory containing Python modules.
    * [watcher.py](Modules/watcher.py): Module defining logic to monitor directories for file changes.
* [main.py](main.py): Python script to run this project.
* [README.md](README.md): This file.
* [requirements.txt](requirements.txt): Text file listing required packages and versions.
