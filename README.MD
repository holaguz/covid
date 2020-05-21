# covid.py

## Installation

Install the dependencies

```bash
pip install -r requirements.txt
```

## Usage

```bash
python3 covid.py [country]
```
Fetch and plot the country data from an API. If you don't pass the ``[country]`` parameter it gets the data from the .xlsx files in the root dir.

Lots of parameters like the start date for plotting are hardcoded. Also install the provided font otherwise it will use some other default font.

