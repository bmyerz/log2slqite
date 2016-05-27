from grappa import GrappaExperiment, MPIRunGrappaExperiment

"""
A place to keep a bunch of example experiments.

Feel free to use this script while developing experiments.

But, when saving things for reproducibility, put each of your final experiments in a separate file
"""


# tpch
tpch_sampa = GrappaExperiment({
    'trial': range(1, 3 + 1),
    'qn': range(1, 22 + 1),
    'exe': lambda qn: "grappa_tpc_q{0}.exe".format(qn),
    'sf': 10,
    'ppn': 12,
    'nnode': 8,
    'query': lambda qn: 'q{0}'.format(qn),
    'vtag': 'v1',
    'machine': 'sampa'
},
{
    'shared_pool_memory_fraction': 0.5
    })


tpch_pal = GrappaExperiment({
    'trial': range(1, 3 + 1),
    'qn': range(1, 22 + 1),
    'exe': lambda qn: "grappa_tpc_q{0}.exe".format(qn),
    'sf': 10,
    'ppn': 16,
    'nnode': 16,
    'query': lambda qn: 'q{0}'.format(qn),
    'vtag': 'v1',
    'machine': 'pal'
},
{
    'shared_pool_memory_fraction': 0.5
    })

tpch_bigdatann = MPIRunGrappaExperiment({
                                'trial': range(1, 3 + 1),
                                'qn': range(1, 22 + 1),
                                'exe': lambda qn: "grappa_tpc_q{0}.exe".format(qn),
                                'sf': 10,
                                'ppn': 16,
                                'nnode': 16,
                                'np': lambda ppn, nnode: ppn*nnode,
                                'query': lambda qn: 'q{0}'.format(qn),
                                'vtag': 'v1',
                                'machine': 'bigdata',
                                'system': 'radish'
                            },
                            {
                                'shared_pool_memory_fraction': 0.5
                            })

tpch_iter_bigdatann = MPIRunGrappaExperiment({
                                'trial': range(1, 3 + 1),
                                #'qn': range(1, 22 + 1),
                                'qn': [6,11,12,14,15,17,19],
                                'exe': lambda qn: "grappa_tpc_iter_q{0}.exe".format(qn),
                                'sf': 10,
                                'ppn': 16,
                                'nnode': 16,
                                'np': lambda ppn, nnode: ppn*nnode,
                                'query': lambda qn: 'q{0}'.format(qn),
                                'vtag': 'v1',
                                'machine': 'bigdata',
                                'system': 'radish-iter'
                            },
                            {
                                'shared_pool_memory_fraction': 0.5
                            })

tpch_bigdatann_debug = MPIRunGrappaExperiment({
                                'trial': range(1, 3 + 1),
                                'qn': [18,19],
                                'exe': lambda qn: "grappa_tpc_q{0}.exe".format(qn),
                                'sf': 10,
                                'ppn': 16,
                                'nnode': 16,
                                'np': lambda ppn, nnode: ppn*nnode,
                                'query': lambda qn: 'q{0}'.format(qn),
                                'vtag': 'v2-debugmode',
                                'machine': 'bigdata',
                                'system': 'radish'
                            },
                            {
                                'shared_pool_memory_fraction': 0.5
                            })

#tpch_bigdatann.run()
#tpch_bigdatann_debug.run()
tpch_iter_bigdatann.run()
