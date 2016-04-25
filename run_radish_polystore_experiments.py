from grappa import MPIRunGrappaExperiment
from itertools import product

mm_datasets = ['random_N_{0}_r_{1}.matrix.dat'.format(sp, si)
               for (sp, si) in product(['10k', '20k', '50k'],
                                       [1.2, 1.3, 1.4, 1.5, 1.6])] + [
    'soc-Pokec.matrix.dat',
    'web-BerkStan.matrix.dat',
    'web-Stanford.matrix.dat']

undir_datasets = ['undirNet_{0}_sm.matrix.dat'.format(s)
                  for s in [1000]]

mm_expers = MPIRunGrappaExperiment({
                                'trial': range(1, 3 + 1),
                                'query': ['sparseMatMultQuery_MyriaL', 'threeSparseMatMultQuery_MyriaL'],
                                'exe': lambda query: "{0}.exe".format(query),
                                'ppn': 4,
                                'nnode': 16,
                                'np': lambda ppn, nnode: ppn*nnode,
                                'vtag': 'v0',
                                'machine': 'r3.xlarge',
                                'system': 'radish',
                            },
                            {
                                #'shared_pool_memory_fraction': 0.5,
                                'input_file_matrix': mm_datasets
                            },
                            hostfile='/etc/hosts')

undir_exps = MP = MPIRunGrappaExperiment({
    'trial': range(1, 3 + 1),
    'query': ['MCL_MyriaL'],
    'exe': lambda query: "{0}.exe".format(query),
    'ppn': 4,
    'nnode': 16,
    'np': lambda ppn, nnode: ppn*nnode,
    'vtag': 'v0',
    'machine': 'r3.xlarge',
    'system': 'radish',
},
    {
        #'shared_pool_memory_fraction': 0.5,
        'input_file_matrix': undir_datasets
    },
    hostfile='/etc/hosts')

mm_expers.run()
undir_exps.run()
