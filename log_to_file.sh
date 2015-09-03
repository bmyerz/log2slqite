set -o nounset

here=$1
script=$here/$2
logfile=$3

export PYTHONPATH=$here
python $script 2>&1 >$logfile
