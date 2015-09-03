set -o nounset

here=$1
script=$2
file=$3

export PYTHONPATH=$here
python $script 2>&1 >$file
