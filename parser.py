from abc import abstractmethod


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


