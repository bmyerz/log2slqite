from grappa import GrappaExperiment, MPIRunGrappaExperiment

tpch_iter_bigdatann = MPIRunGrappaExperiment({
                                'trial': range(1, 3 + 1),
                                'qn': [4,11,12,16,17,18],#[x for x in range(1, 20 + 1)],
                                'exe': lambda qn: "grappa_tpc_iter_q{0}_gbp.exe".format(qn),
                                'sf': 10,
                                'ppn': 16,
                                'nnode': 16,
                                'np': lambda ppn, nnode: ppn*nnode,
                                'query': lambda qn: 'q{0}'.format(qn),
                                'vtag': 'v3-no-compile-bugs',
                                'machine': 'bigdata',
                                'system': 'radish-iter-gbp'
                            },
                            {
                                'shared_pool_memory_fraction': 0.5
                            })

tpch_iter_sampa = GrappaExperiment({
                                'trial': range(1, 3 + 1),
                                'qn': [x for x in range(1, 20 + 1)],
                                'exe': lambda qn: "grappa_tpc_iter_q{0}_gbp.exe".format(qn),
                                'sf': 10,
                                'ppn': 12,
                                'nnode': 16,
                                'np': lambda ppn, nnode: ppn*nnode,
                                'query': lambda qn: 'q{0}'.format(qn),
                                'vtag': 'align-fix',
                                'machine': 'sampa',
                                'system': 'radish-iter-gbp'
                            },
                            {
                                'shared_pool_memory_fraction': 0.5
                            })

#tpch_iter_bigdatann.run()
tpch_iter_sampa.run()
