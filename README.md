# CSVMagic

[![Python 3.9](https://img.shields.io/badge/python-3.9-greensvg)](https://www.python.org/downloads/release/python-390/)

CSV Reader

This CSV reader is implemented in Python. It allows to specify a separator, a quote char and
column titles (or get the first row as titles). 

## Installation

Install it with:

```shell
pip install csvMagic
```

## Usage

The usage mimics the behaviour of the CSV python module's DictReader:

```python
from csvMagic import CSVMagic

for row in CSVMagic().read_file("csvFile.csv"):
    print(row)
```

This reads and iterates over the `csvFile.csv` file as a key-value dictionary. Accepted line endings are `\n` or `\r\n`.
Files are opened in text-mode with `utf-8` encoding by default using the read_file function but other streams can be supplied
directly to the read() function.

```python
from csvMagic import CSVMagic

with open("csvFile.csv") as file:
    for row in CSVMagic().read(file):
        print(row)
```

    Note: Blank lines in the file are ignored.

### Parameters

CSVMagic can be parameterised with different behaviours during initialisation. The default
parameters are shown below:

```python
from csvMagic import CSVMagic

csv_reader = CSVMagic(
    separator=",",
    quote_char='"',
    field_names = None,
    strict=True,
    has_headers=False
)
```

Available settings:

 * `separator`: character used as separator (defaults to `,`)
 * `quote_char`: character used to quote strings (defaults to `"`).<br />
    This char can be escaped by duplicating it.
 * `field_names`: can be any iterable or sequence of `str`.<br />
    If set, these will be used as column headers (i.e. dictionary keys). Also sets the expected number of columns.</br>
 * `strict`: Sets whether the parser runs in _strict mode_ or not.<br />
    In _strict mode_ the parser will raise a `ValueError` exception if a cell cannot be decoded or column
    numbers don't match. In _non-strict mode_ non-recognized cells will be returned as strings. If there are more
    columns than expected they will be ignored. If there are less, the dictionary will contain fewer values.
 * `has_headers`: whether the first row should be taken as column titles or not.<br />
    If set, `field_names` cannot be specified. If not set, and no field names are specified, dictionary keys will
    be just the column positions of the cells.

 
## Recognised data types

The parser recognises the following cell types:

 * `None` (empty values). Unlike CSV reader, it will return `None` (null) for empty values. <br />
    Empty strings (`""`) are recognized correctly.
 * `str` (strings): Anything that is quoted with the `quotechar`. Default quotechar is `"`. <br />
    If the string contains a quote, it must be escaped by duplicating it. i.e. `"Duplicate "" Quote """` decodes
    to `"Duplicate "Quote""` string.
 * `int` (integers):  any integer recognized by Python
 * `float`: any float recognized by Python
 * `datetime`: a datetime in ISO format (with 'T' or whitespace in the middle), like `2022-02-19 17:39:02`
 * `date`: a date in ISO format, like `2022-02-19`
 * `time`: a time in ISO format, like `17:39:02`
 
Parsing attempts are tried in their respective order as presented above. If the cell does not meet any of the specified
type criteria, a string is returned. However, if `strict_mode` is set to `True`, a `ValueError` exception is raised.

## Why was this created

This module offers a simplified version of the existing CSV module and provides greater transparency behind the processes
involved in reading CSV files. CSV is a commonly-used format of exchanging tabular data between spreadsheets and relational
databases. Understanding the functionalities hidden in the CSV library is therefore an important and valuable skill for
developers.
