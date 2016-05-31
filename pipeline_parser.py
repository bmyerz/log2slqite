import itertools
import re
from parameters import JSONParamsParser, PARAMS_TAG
from log2sqlite import cli
from parser import Parser


class PipelineLogParser(Parser):
    _time_pat = re.compile(r'pipeline (?P<num>\d+): (?P<time>\d+[.]\d+) s')  # pipeline 1: 0.53401 s
    _start_pat = re.compile(r'timestamp (?P<num>\d+) start (?P<time>\d+[.]\d+)')
    _end_pat = re.compile(r'timestamp (?P<num>\d+) end (?P<time>\d+[.]\d+)')

    def recorditer(self, inputstr):
        jparams = JSONParamsParser(PARAMS_TAG)
        assert jparams.count(inputstr) == 1, "Cannot process logs with more than one record"

        for pdict in itertools.izip(jparams.idict_from_json(inputstr)):

            piperesults = {}

            # process the total times
            for m in re.finditer(self._time_pat, inputstr):
                num = m.group('num')
                time = m.group('time')
                d = piperesults.get(num, {})
                d['time'] = time

            # process the starts
            for m in re.finditer(self._start_pat, inputstr):
                num = m.group('num')
                time = m.group('time')
                d = piperesults.get(num, {})
                d['start'] = time

            # process the ends
            for m in re.finditer(self._end_pat, inputstr):
                num = m.group('num')
                time = m.group('time')
                d = piperesults.get(num, {})
                d['end'] = time

            # combine into records
            for num, d in piperesults.iteritems():
                d['num'] = num
                cr = pdict.copy()
                cr.update(d)
                yield cr

if __name__ == '__main__':
    cli(PipelineLogParser())
