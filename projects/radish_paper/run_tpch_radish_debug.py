from grappa import GrappaExperiment, MPIRunGrappaExperiment

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

tpch_bigdatann_debug.run()
