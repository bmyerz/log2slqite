import re
from log2sqlite import Parser, cli


class ImpalaLogParser(Parser):

    def recorditer(self, inputstr):
        querypat = r'Running Impala query: (q\d+)[_a-z]+'
        timepat = r'Time:(\d+[.]\d+)'
        secondpat = r'and a second time: (q\d+)'

        for m in re.finditer(querypat, inputstr):
            r = {'machine': 'bigdata', 'nnode': 16 } # hardcoded params

            r['query'] = m.group(1)
            mt = re.search(timepat, inputstr[m.end():])
            r['runtime1'] = mt.group(1)
            ms = re.search(secondpat, inputstr[mt.end():])
            assert r['query'] == ms.group(1), \
                "First and second runs are not the same query {0} {1}".format(
                    r['query'], ms.group(1)
                )
            mt2 = re.search(timepat, inputstr[ms.end():])
            r['runtime2'] = mt2.group(1)
            yield r


cli(ImpalaLogParser())