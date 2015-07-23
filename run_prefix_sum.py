import json
import sys
import subprocess

grappa_srun = '../../bin/grappa_srun'

cmd_template = """{0} \
                        --ppn={{ppn}} \
                        --nnode={{nnode}} \
                        -- \
                        ./{{exe}} \
                        --tuples_per_core={{tuples_per_core}} \
                        2>&1""".format(grappa_srun)

for trial in [1, 2, 3]:
    for transformation in ["fused", "split"]:
        params = {
            'exe': "grappa_loop_prefix_sum_{0}.exe".format(transformation),
            'transformation': transformation,
            'ppn': 12,
            'nnode': 10,
            'trial': trial,
            'tuples_per_core': 1024*1024*50,
            'vtag': 'v3'
        }

        paramsjson = json.dumps(params)
        print "PARAMS{0}PARAMS".format(paramsjson)

        cmd = cmd_template.format(**params)
        subprocess.check_call(cmd, shell=True)
