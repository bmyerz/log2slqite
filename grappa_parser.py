import itertools
import json
import re
from log2sqlite import Parser, cli

__author__ = 'brandon'


class GrappaLogParser(Parser):
    _paramjsonpat = re.compile(r'PARAMS{[^}]+}PARAMS')
    _statjsonpat = re.compile(r'STATS{[^}]+}STATS')
    _frontpat = re.compile(r'0+:')
    _statspat = re.compile(r'STATS')
    _paramspat = re.compile(r'PARAMS')
    _lastcomma = re.compile(r',[^",}]+}') # if one exists

    def __init__(self, includes_params=True):
        self.includes_params = includes_params

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

        LOG(notrailing)
        asdict = json.loads(notrailing)
        return asdict

    def recorditer(self, inputstr):
        if self.includes_params:
            # concurrently search for adjacent pairs of PARAMS and STATS
            for praw, sraw in itertools.izip(
                    re.finditer(self._paramjsonpat, inputstr),
                    re.finditer(self._statjsonpat, inputstr)):

                result = {}
                result.update(self._raw_to_dict(praw, self._paramspat))
                result.update(self._raw_to_dict(sraw, self._statspat))
                yield result
        else:
            for sraw in itertools.izip(
                    re.finditer(self._statjsonpat, inputstr)):

                result = {}
                result.update(self._raw_to_dict(sraw, self._statspat))
                yield result


if __name__ == '__main__':
    cli(GrappaLogParser())
