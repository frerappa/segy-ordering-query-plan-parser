# segy-ordering-qp-parser

This project implements a parser that translates a "Query Plan" for a SEG-Y file ordering tool to SQL.
SEG-Y is a file format commonly used to store seismic data. The Query Plan is a simple DSL intended to ease the 
usage of a tool that can order and filter data in multiple SEG-Y files in parallel, developed in a different project.

## Requirements

- Python 3.9+
- [SLY](https://sly.readthedocs.io/en/latest/sly.html) is a parsing library that should be cloned from [GitHub](https://github.com/dabeaz/sly) in the `lib` folder. 
 
## Installation

The project`s path should be installed using
````bash
pip install -e .
````

## Usage 
By default, the projects only provides a single class as an importable object, `QueryPlanToSQL`. It currently has a single 
method `translate`, which takes in a string with the Query Plan (as described in `/doc`) and outputs an equivalent SQL query. The 
optimization and handling of the resulting SQL query is not in the scope of this project.


