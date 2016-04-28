# log2sqlite

log2sqlite provides simple utilities for running experiments and collecting results.

The workflow is broken into two steps: 

1. run experiments and generate log files
2. parse logs into a more useful format (e.g., a sqlite table)

The two components can be used independently.

## Running experiments

An experiment (or collection of experiments) is described declaratively as a dictionary
mapping parameter names to parameter values. A parameter's value can be a single value,
a list of values, or a function to produce a value. log2sqlite takes the product of all
parameter values to enumerate a list of experiments.

## Parsing log files to store in sqlite

### Setup

log2sqlite uses [dataset](http://dataset.readthedocs.io/en/latest/) for working with tables.

```bash
pip install dataset
```

### Try it

`log2sqlite.run` takes the log as a string, a `Parser`, and a `Processor`. A `Parser` produces records (as python dictionaries) and a `Processor` does something with each record.

as an example, see and run the test
```bash
test/run_test.sh
```

