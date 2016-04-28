import sys
import json


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
        print "PARAMS{0}PARAMS".format(paramsjson)
        sys.stdout.flush()


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



