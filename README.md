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

See examples in the `projects/` directory.

### Use one parameter to set another

You can make parameter values depend on others. This is super useful in a lot of
situations. For example, imagine you have a parameter `scale`, valued 1, 10, 100, and
corresponding input files `data_scale_1`, `data_scale_10`, `data_scale_100`. 
You can set these parameters by:

```python
{...
  scale: [1, 10, 100],
  inputfile: lambda scale: "data_scale_{}".format(scale)
  ...
}
```

The only restriction is that the function you give as the parameter value
must have arguments that are other parameter names. 

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

