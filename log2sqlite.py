import re
import json
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
    for r in parser.recorditer(inputstr):
        processor.processrecord(r)

    processor.close()

