from grappa import GrappaExperiment

# fusion
fusion_split = GrappaExperiment({
    'transformation': ["fused", "split"],
    'exe': lambda transformation: "grappa_loop_prefix_sum_{0}.exe".format(
        transformation),
    'ppn': 12,
    'nnode': 10,
    'trial': range(1, 3 + 1),
    'vtag': 'v3'
},
grappa_params={
    'tuples_per_core': 1024*1024*50,
})

fusion_split.run()


