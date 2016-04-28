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




