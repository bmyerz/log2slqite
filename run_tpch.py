from grappa import GrappaExperiment

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

tpch_pal.run()
