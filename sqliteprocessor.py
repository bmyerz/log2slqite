from parser import Processor
import dataset


class SQLiteProcessor(Processor):

    def __init__(self, dbname, tablename):
        self.db = dataset.connect('sqlite:///{0}'.format(dbname))
        self.table = self.db[tablename]

    def processrecord(self, record):
        for k in self.table.columns:
          if not k in record:
            record[k] = None   # for missing columns put None

        self.table.insert(record)

    def close(self):
        pass