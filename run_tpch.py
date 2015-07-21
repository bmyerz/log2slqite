import json
import subprocess

grappa_srun = '../../bin/grappa_srun'

cmd_template = """{0} \
                        --ppn={{ppn}} \
                        --nnode={{nnode}} \
                        -- \
                        ./{{exe}} \
                        2>&1""".format(grappa_srun)

for trial in [1, 2, 3, 4]:
    for qn in [1,2,3]:
        params = {
            'exe': "grappa_tpc_q{0}.exe".format(qn),
            'sf': 10,
            'ppn': 12,
            'nnode': 8,
            'query': 'q{0}'.format(qn),
            'trial': trial,
            'vtag': 'v1'
        }

        paramsjson = json.dumps(params)
        print "PARAMS{0}PARAMS".format(paramsjson)

        cmd = cmd_template.format(**params)
        subprocess.check_call(cmd, shell=True)
