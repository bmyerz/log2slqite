from grappa import MPIRunGrappaExperiment
from itertools import product
from grappa_parser import GrappaLogParser

mm_datasets = ['random_N_{0}_r_{1}.matrix.dat'.format(sp, si)
               for (sp, si) in product(['10k', '20k', '50k'],
                                       [1.2, 1.3, 1.4, 1.5, 1.6])] + [
    'soc-Pokec.matrix.dat',
    'web-BerkStan.matrix.dat',
    'web-Stanford.matrix.dat']
mm_datasets.remove('random_N_{0}_r_{1}.matrix.dat'.format('20k', 1.6))
mm_datasets.remove('random_N_{0}_r_{1}.matrix.dat'.format('50k', 1.5))
mm_datasets.remove('random_N_{0}_r_{1}.matrix.dat'.format('50k', 1.6))

undir_datasets = ['undirNet_{0}_sm.matrix.dat'.format(s)
                  for s in [1000]]

with open("~/results/polystore_exps.log") as f:
    existing_logs = f.read()

mm_expers = MPIRunGrappaExperiment({
    'trial': range(1, 3 + 1),
    'query': ['grappa_sparseMatMultQuery_MyriaL', 'grappa_threeSparseMatMultQuery_MyriaL'],
    'exe': lambda query: "{0}.exe".format(query),
    'ppn': 4,
    'nnode': 16,
    'np': lambda ppn, nnode: ppn * nnode,
    'vtag': 'v0',
    'machine': 'r3.xlarge',
    'system': 'radish',
    'hostfile': '~/hostfile'
},
    {
    #'shared_pool_memory_fraction': 0.5,
    'input_file_matrix': mm_datasets
},

    "cp ~/data2/{input_file_matrix}.bin ~/data; sleep 1",
    "rm ~/data/{input_file_matrix}.bin",
    GrappaLogParser().recorditer(existing_logs)
)

undir_exps = MP = MPIRunGrappaExperiment({
    'trial': range(1, 3 + 1),
    'query': ['grappa_MCL_MyriaL'],
    'exe': lambda query: "{0}.exe".format(query),
    'ppn': 4,
    'nnode': 16,
    'np': lambda ppn, nnode: ppn * nnode,
    'vtag': 'v0',
    'machine': 'r3.xlarge',
    'system': 'radish',
    'hostfile': '~/hostfile'
},
    {
        #'shared_pool_memory_fraction': 0.5,
        'input_file_graph': undir_datasets
},
    "cp ~/data2/{{input_file_graph}}.bin ~/data; sleep 1",
    "rm ~/data/{{input_file_graph}}.bin",
    GrappaLogParser().recorditer(existing_logs)
)

mm_expers.run()
undir_exps.run()
