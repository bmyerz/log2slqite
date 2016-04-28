import sys
import json
import re
from log2sqlite import LOG


PARAMS_TAG = 'PARAMS'


class ParameterUtils(object):
    @staticmethod
    def require_params(required, params):
        for r in required:
            if not (r in params):
                raise Exception("require parameter {0}".format(r))

    @staticmethod
    def print_params_as_json(params):
        """
        for recordparams that outputs parameters as a JSON string
        PARAMS{ "myparam": "paramvalue", ...}PARAM
        """
        paramsjson = json.dumps(params)
        print "{1}{0}{1}".format(paramsjson, PARAMS_TAG)
        sys.stdout.flush()


class JSONParamsParser(object):
    _lastcomma = re.compile(r',[^",}]+}') # if one exists
    _frontpat = re.compile(r'0+:')

    def __init__(self, tag):
        self._taggedjsonpat = re.compile(r'TAG{[^}]+}TAG'.replace('TAG', tag))
        self._tagpat = re.compile(r'TAG'.replace('TAG', tag))

    def idict_from_json(self, input_str):
        for raw in re.finditer(self._taggedjsonpat, input_str):
            yield self._raw_to_dict(raw)

    def _raw_to_dict(self, raw):
        # find the next experimental result
        found = raw.group(0)

        # remove STATS tags
        notags = re.sub(self._tagpat, '', found)

        # remove mpi logging node ids
        noids = re.sub(self._frontpat, '', notags)

        # json doesn't allow trailing comma
        notrailing = re.sub(self._lastcomma, '}', noids)

        LOG(notrailing)
        asdict = json.loads(notrailing)
        return asdict




# An alternative to using ParameterUtils imperatively is to use them
# declaratively. Mixin these classes to your Experiment subclass.
# Each of these parameter mixins will be automatically chained together.


def _call_super_if_exists(clazz, self, params):
    if hasattr(super(clazz, self), 'recordparams'):
        getattr(super(clazz, self))(params)


class RequiredParams(object):
    """Mixin class for subclasses of Experiment to provide
    required parameters. To use, also provide class variable
    _required
    """
    _required = []

    def recordparams(self, params):
        if len(self._required) == 0:
            raise ValueError("Mixing in RequiredParams requires at least one required param")

        ParameterUtils.require_params(self._required, params)

        _call_super_if_exists(RequiredParams, self)


class JSONParams(object):
    """Mixin class for subclasses of Experiment to provide a
    recordparams that outputs parameters as a JSON string
    PARAMS{ "myparam": "paramvalue", ...}PARAM
    """
    def recordparams(self, params):
        ParameterUtils.print_params_as_json(params)

        _call_super_if_exists(RequiredParams, self)



