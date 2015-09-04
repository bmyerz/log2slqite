from grappa import GrappaExperiment, MPIRunGrappaExperiment

tpch_iter_bigdatann = MPIRunGrappaExperiment({
                                'trial': range(1, 3 + 1),
                                'qn': range(1, 22 + 1),
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

tpch_iter_bigdatann.run()
