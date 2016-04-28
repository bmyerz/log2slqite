import argparse
import sys
import common

from sqliteprocessor import SQLiteProcessor


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
    common.logging = args.verbose

    with open(args.inputf, 'r') as inf:
        run(inf.read(),
            parser,
            SQLiteProcessor(args.dbname, args.tablename))