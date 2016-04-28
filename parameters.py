import sys
import json


def _call_super_if_exists(clazz, self, params):
    if hasattr(super(clazz, self), 'recordparams'):
        getattr(super(clazz, self))(params)

# Each of these parameter mixins will be chained together


class RequiredParams(object):
    """Mixin class for subclasses of Experiment to provide
    required parameters. To use, also provide class variable
    _required
    """
    _required = []

    def recordparams(self, params):
        if len(self._required) == 0:
            raise ValueError("Mixing in RequiredParams requires at least one required param")

        for r in self._required:
            if not (r in params):
                raise Exception("require parameter {0}".format(r))

        _call_super_if_exists(RequiredParams, self)


class JSONParams(object):
    """Mixin class for subclasses of Experiment to provide a
    recordparams that outputs parameters as a JSON string
    PARAMS{ "myparam": "paramvalue", ...}PARAM
    """
    def recordparams(self, params):
        paramsjson = json.dumps(params)
        print "PARAMS{0}PARAMS".format(paramsjson)
        sys.stdout.flush()

        _call_super_if_exists(RequiredParams, self)


