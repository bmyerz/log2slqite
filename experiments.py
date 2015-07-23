import collections
import inspect
import subprocess
from abc import abstractmethod


class Experiment(object):

    def __init__(self, params):
        self.params_lists = params

    @staticmethod
    def _call_with_relevant_params(f, p, name=None):
        """
        Given a function and a superset of parameter
        bindings, call the function on its named parameters
        """

        # find the relevant named parameters
        argnames = set(inspect.getargspec(f).args)

        dused = dict([e for e in p.items()
                      if e[0] in argnames])

        if len(dused) < len(argnames):
            raise Exception("Resolving {0} without parameters {1}".format(
                name, set(argnames) - set(dused)))

        # apply f
        return f(**dused)

    @staticmethod
    def _enumerate_experiments(d, keys, depth=0):
        """
        Given parameters and lists of assignments,
        return the crossproduct of all parameter assignments
        """

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
                                    Experiment._call_with_relevant_params(av, params_assigned, ak)

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
        """
        Record the parameter assignments in experimental logs.
        """
        pass

    @abstractmethod
    def cmd(self):
        """
        Return the cmd template, which will be filled in with parameters
        """
        pass


