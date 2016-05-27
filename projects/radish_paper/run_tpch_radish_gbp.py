from grappa import GrappaExperiment, MPIRunGrappaExperiment

tpch_bigdatann = MPIRunGrappaExperiment({
                                'trial': range(1, 3 + 1),
                                'qn': [x for x in range(1, 20 + 1) if x!=7],  # Q7 is slow
                                'exe': lambda qn: "grappa_tpc_q{0}_gbp.exe".format(qn),
                                'sf': 10,
                                'ppn': 16,
                                'nnode': 16,
                                'np': lambda ppn, nnode: ppn*nnode,
                                'query': lambda qn: 'q{0}'.format(qn),
                                'vtag': 'v1',
                                'machine': 'bigdata',
                                'system': 'radish-gbp-noalign'
                            },
                            {
                                'shared_pool_memory_fraction': 0.5
                            })


tpch_bigdatann.run()
