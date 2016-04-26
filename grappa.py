import json
from experiments import Experiment
import sys


class GrappaExperiment(Experiment):
    _required = ["ppn", "nnode"]

    def __init__(self, params, grappa_params={}, setup=None, teardown=None):
        # grappa_params are command line arguments
        self.grappa_param_names = grappa_params.keys()
        all_params = {}
        all_params.update(params)
        all_params.update(grappa_params)
	self.setup = setup
	self.teardown = teardown
        super(GrappaExperiment, self).__init__(all_params)

    def cmd(self):
        clargs_template = '--{name}={{{name}}}'
        clargs = ' '.join([clargs_template.format(name=n) for n in self.grappa_param_names])

        cmd_template = self._cmd_template().format(clargs=clargs)

	if self.setup is not None:
		cmd_template = self.setup + '; ' + cmd_template
	if self.teardown is not None:
		cmd_template = cmd_template + '; ' + self.teardown

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

    def __init__(self, params, grappa_params, setup=None, teardown=None):
	if 'hostfile' not in params:
		params['hostfile'] = '/people/bdmyers/hadoop.hosts'
		print "Using default hostfile {0}".format(params['hostfile'])
        super(MPIRunGrappaExperiment, self).__init__(params, grappa_params, setup, teardown)

    def _cmd_template(self):
        return """mpirun \
                     --hostfile {{hostfile}} \
                     -np {{np}} \
                     ./{{exe}} \
                     {clargs} \
                     2>&1"""
