import json
from experiments import Experiment


class GrappaExperiment(Experiment):
    _required = ["ppn", "nnode"]

    def __init__(self, params, grappa_params={}):
        # grappa_params are command line arguments
        self.grappa_param_names = grappa_params.keys()
        all_params = {}
        all_params.update(params)
        all_params.update(grappa_params)
        super(GrappaExperiment, self).__init__(all_params)

    def cmd(self):
        grappa_srun = '../../bin/grappa_srun'

        clargs_template = '--{name}={{{name}}}'
        clargs = ' '.join([clargs_template.format(name=n) for n in self.grappa_param_names])

        cmd_template = """{0} \
                                --ppn={{ppn}} \
                                --nnode={{nnode}} \
                                -- \
                                ./{{exe}} \
                                {1} \
                                2>&1""".format(grappa_srun, clargs)
        return cmd_template

    def recordparams(self, params):
        for r in self._required:
            if not (r in params):
                raise Exception("require parameter {0}".format(r))

        paramsjson = json.dumps(params)
        print "PARAMS{0}PARAMS".format(paramsjson)


