# plook


**Table of Contents**

- [Installation](#installation)
- [License](#license)

## Installation

```console
pip install plook
```

## License

`plook` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.

Two versions of file binary search in python. Look.py uses mmap while
SLook.py uses only standard file I/O


## SLook
usage: SLook.py [-h] [--file FILE] --key KEY [--fold]

file binary search

options:
  -h, --help   show this help message and exit
  --file FILE  sorted text file to search
  --key KEY    word to search
  --fold       fold case - case independent search

## Look

Usage: Look.py [options]

Options:
  -h, --help  show this help message and exit
  -f, --fold  ignore case
