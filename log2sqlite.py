import argparse
import sys
from abc import abstractmethod

from sqliteprocessor import SQLiteProcessor

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


def run(inputstr, parser, processor):
    count = 0
    for r in parser.recorditer(inputstr):
        processor.processrecord(r)
        count += 1

    processor.close()
    print "processed {0} records".format(count)


def cli(parser):
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
