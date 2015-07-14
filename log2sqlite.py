import re
import sys
import json
import argparse
import dataset
import json
from abc import abstractmethod


class Parser(object):

    @abstractmethod
    def recorditer(self, inputstr):
        pass


class GrappaLogParser(Parser):
    _runpat = re.compile(r'STATS{[^}]+}STATS')
    _frontpat = re.compile(r'00:')
    _statspat = re.compile(r'STATS')
    _lastcomma = re.compile(r',[^,}]+}')

    def recorditer(self, inputstr):
        for r in re.finditer(self._runpat, inputstr):
            # find the next experimental result
            found = r.group(0)

            # remove STATS tags
            notags = re.sub(self._statspat, '', found)

            # remove mpi logging node ids
            noids = re.sub(self._frontpat, '', notags)

            # json doesn't allow trailing comma
            notrailing = re.sub(self._lastcomma, '}', noids)

            asdict = json.loads(notrailing)

            yield asdict


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
