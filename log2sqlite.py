import re
import sys
import json
import itertools
import argparse
import dataset
import json
from abc import abstractmethod


class Parser(object):

    @abstractmethod
    def recorditer(self, inputstr):
        pass


class GrappaLogParser(Parser):
    _paramjsonpat = re.compile(r'PARAMS{[^}]+}PARAMS')
    _statjsonpat = re.compile(r'STATS{[^}]+}STATS')
    _frontpat = re.compile(r'00:')
    _statspat = re.compile(r'STATS')
    _paramspat = re.compile(r'PARAMS')
    _lastcomma = re.compile(r',[^,}]+}')

    @classmethod
    def _raw_to_dict(cls, raw, tagpattern):
        # find the next experimental result
        found = raw.group(0)

        # remove STATS tags
        notags = re.sub(tagpattern, '', found)

        # remove mpi logging node ids
        noids = re.sub(cls._frontpat, '', notags)

        # json doesn't allow trailing comma
        notrailing = re.sub(cls._lastcomma, '}', noids)

        asdict = json.loads(notrailing)
        return asdict

    def recorditer(self, inputstr):
        # concurrently search for adjacent pairs of PARAMS and STATS
        for praw, sraw in itertools.izip(
                re.finditer(self._paramjsonpat, inputstr),
                re.finditer(self._statjsonpat, inputstr)):

            result = {}
            result.update(self._raw_to_dict(praw, self._paramspat))
            result.update(self._raw_to_dict(sraw, self._statspat))
            yield result


class Processor(object):

    @abstractmethod
    def processrecord(self, record):
        pass

    @abstractmethod
    def close(self):
        pass


class SQLiteProcessor(Processor):

    def __init__(self, dbname, tablename):
        self.db = dataset.connect('sqlite:///{0}'.format(dbname))
        self.table = self.db[tablename]

        # bulk insert
        self.db.begin()

    def processrecord(self, record):
        self.table.insert(record)

    def close(self):
        # end bul insert
        self.db.commit()


def run(inputstr, parser, processor):
    count = 0
    for r in parser.recorditer(inputstr):
        processor.processrecord(r)
        count += 1

    processor.close()
    print "processed {0} records".format(count)

if __name__ == '__main__':
    p = argparse.ArgumentParser(prog=sys.argv[0])
    p.add_argument("-d", dest="dbname", required=True, help="database name")
    p.add_argument("-t", dest="tablename", required=True, help="table name")
    p.add_argument("-i", dest="inputf", required=True,
                   help="input log file; may contain multiple records")

    args = p.parse_args(sys.argv[1:])

    with open(args.inputf, 'r') as inf:
        run(inf.read(),
            GrappaLogParser(),
            SQLiteProcessor(args.dbname, args.tablename))
