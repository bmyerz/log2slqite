import sys
import argparse
from abc import abstractmethod
import dataset


logging = False


def LOG(s):
    if logging:
        if type(s).__name__ == "str":
            print s
        else:
            print str(s)


class Parser(object):

    @abstractmethod
    def recorditer(self, inputstr):
        pass


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
        self.rows_to_insert = []

    def processrecord(self, record):
        for k in self.table.columns:
          if not k in record:
            record[k] = None   # for missing columns put None

        self.rows_to_insert.append(record)

    def close(self):
        self.table.insert_many(self.rows_to_insert)


def run(inputstr, parser, processor):
    count = 0
    for r in parser.recorditer(inputstr):
        processor.processrecord(r)
        count += 1

    processor.close()
    print "processed {0} records".format(count)


def cli(parser):
    if __name__ == '__main__':
        p = argparse.ArgumentParser(prog=sys.argv[0])
        p.add_argument("-d", dest="dbname", required=True, help="database name")
        p.add_argument("-t", dest="tablename", required=True, help="table name")
        p.add_argument("-i", dest="inputf", required=True,
                       help="input log file; may contain multiple records")
        p.add_argument("-v", dest="verbose", action="store_true", help="turn on verbose logging")

        args = p.parse_args(sys.argv[1:])
        logging = args.verbose

        with open(args.inputf, 'r') as inf:
            run(inf.read(),
                parser,
                SQLiteProcessor(args.dbname, args.tablename))
