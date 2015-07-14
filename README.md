# log2slqite

Parse logs into a sqlite table

## Setup

```bash
pip install dataset
```

## Try it

`log2sqlite.run` takes the log as a string, a `Parser`, and a `Processor`. A `Parser` produces records (as python dictionaries) and a `Processor` does something with each record.

`test.py` contains an example  
