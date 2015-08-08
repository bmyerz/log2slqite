import re
from log2sqlite import Parser, cli


class ImpalaLogParser(Parser):
    def recorditer(self, inputstr):
        ncodegen = None
        for cg in re.finditer(r'Code generation disabled[?] (\d)', inputstr):
            assert ncodegen is None, "Only one supported in input string"
            ncodegen = int(cg.group(1))
        assert ncodegen is not None, "Missing a code generation on/off parameter"
        assert (ncodegen == 1) or (ncodegen == 0)

        querypat = re.compile(r'Running query: (?P<query>q\d+)[_a-z]+\nTime:(?P<preptime>\d+[.]\d+)\nTime:(?P<runtime1>\d+[.]\d+)\nTime:(?P<runtime2>\d+[.]\d+)\n(?P<failmsg>(ABOVE QUERY FAILED:1)?)')

        for m in re.finditer(querypat, inputstr):
            # hardcoded params
            r = {'machine': 'bigdata',
                 'system': 'impala',
                 'nnode': 16,
                 'codegen': 1-ncodegen
            }

            for k in ['query', 'runtime1', 'runtime2', 'preptime']:
                r[k] = m.group(k)

            if m.group('failmsg') != '':
                print "failed query {0}; not saving".format(r['query'])
                continue

            yield r


if __name__ == '__main__':
    cli(ImpalaLogParser())
