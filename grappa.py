import json
from experiments import Experiment
import sys


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
        clargs_template = '--{name}={{{name}}}'
        clargs = ' '.join([clargs_template.format(name=n) for n in self.grappa_param_names])

        cmd_template = self._cmd_template().format(clargs=clargs)

        return cmd_template

    def recordparams(self, params):
        for r in self._required:
            if not (r in params):
                raise Exception("require parameter {0}".format(r))

        paramsjson = json.dumps(params)
        print "PARAMS{0}PARAMS".format(paramsjson)
        sys.stdout.flush()

    def _cmd_template(self):
        return """../../bin/grappa_srun \
                                --ppn={{ppn}} \
                                --nnode={{nnode}} \
                                -- \
                                ./{{exe}} \
                                {clargs} \
                                2>&1"""


class MPIRunGrappaExperiment(GrappaExperiment):
    _required = ["np"]

    def _cmd_template(self):
        return """mpirun \
                     --hostfile /people/bdmyers/hadoop.hosts \
                     -np {{np}} \
                     ./{{exe}} \
                     {clargs} \
                     2>&1"""
