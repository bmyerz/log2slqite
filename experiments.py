import collections
import json
import inspect
import subprocess
from abc import abstractmethod


class Experiment:

    def __init__(self, params):
        self.params_lists = params

    @staticmethod
    def _call_with_possible_params(f, p, name=None):
        # find the relevant named parameters
        argnames = set(inspect.getargspec(f).args)

        dused = dict([e for e in p.items()
                      if e[0] in argnames])

        if len(dused) < len(argnames):
            raise Exception("Resolving {0} without parameters {1}".format(
                name, set(argnames) - set(dused)))

        # evaluate
        return f(**dused)

    @staticmethod
    def _enumerate_experiments(d, keys, depth=0):
        if len(keys) == 0:
            yield {}
        else:
            k, rest = keys[0], keys[1:]
            vals = d[k]

            # make sure everything is a list of values
            if not isinstance(vals, collections.Iterable):
                vals = [vals]

            for v in vals:

                params_assigned = {k: v}
                for rest_assigned in Experiment._enumerate_experiments(d, rest, depth+1):
                    params_assigned.update(rest_assigned)

                    if depth == 0:
                        # now that all keys are assigned
                        # we can resolve dependent ones
                        for ak, av in params_assigned.items():
                            if isinstance(av, type(lambda x: x)):
                                resolved_val = \
                                    Experiment._call_with_possible_params(av, params_assigned, ak)

                                # replace the function with application
                                params_assigned[ak] = resolved_val

                    yield params_assigned

    def run(self):
        for params in self._enumerate_experiments(
                self.params_lists, self.params_lists.keys()):
            c = self.cmd().format(**params)
            subprocess.check_call(c, shell=True)

    @abstractmethod
    def recordparams(self, params):
        pass

    @abstractmethod
    def cmd(self):
        pass


class GrappaExperiment(Experiment):
    _required = ["ppn", "nnode"]

    def cmd(self):
        grappa_srun = '../../bin/grappa_srun'

        cmd_template = """{0} \
                                --ppn={{ppn}} \
                                --nnode={{nnode}} \
                                --tuples_per_core={{tuples_per_core}} \
                                -- \
                                ./{{exe}} \
                                2>&1""".format(grappa_srun)
        return cmd_template

    def recordparams(self, params):
        for r in self._required:
            if not (r in params):
                raise Exception("require parameter {0}".format(r))

        paramsjson = json.dumps(params)
        print "PARAMS{0}PARAMS".format(paramsjson)


# fusion
fusion_split = GrappaExperiment({
    'transformation': ["fused", "split"],
    'exe': lambda transformation: "grappa_loop_prefix_sum_{0}.exe".format(
        transformation),
    'ppn': 12,
    'nnode': 10,
    'trial': range(1, 3 + 1),
    'tuples_per_core': 1024*1024*50,
    'vtag': 'v3'
})

fusion_split.run()


