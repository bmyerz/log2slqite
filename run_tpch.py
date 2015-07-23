from grappa import GrappaExperiment

# tpch
tpch = GrappaExperiment({
    'trial': range(1, 3 + 1),
    'qn': range(1, 3 + 1),
    'exe': lambda qn: "grappa_tpc_q{0}.exe".format(qn),
    'sf': 10,
    'ppn': 12,
    'nnode': 8,
    'query': lambda qn: 'q{0}'.format(qn),
    'vtag': 'v1'
})

tpch.run()
