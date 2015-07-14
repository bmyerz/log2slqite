import re
import json
import dataset
import json

runpat = re.compile(r'STATS{[^}]+}STATS')
frontpat = re.compile(r'00:')
statspat = re.compile(r'STATS')
lastcomma = re.compile(r',[^,}]+}')

i = re.finditer(runpat, """
    00: STATS{
      00:   "app_1_gce_incomplete": 0,
      00:   "app_2_gce_incomplete": 0,
      00:   "globalq_data_pull_reply_messages": 0,
      00:   "globalq_data_pull_reply_total_bytes": 0,
      00:   "globalq_data_pull_request_num_elements": 0, "globalq_data_pull_request_num_elements_count": 0, "globalq_data_pull_request_num_elements_mean": 0, "globalq_data_pull_request_num_elements_stddev": 0, "globalq_data_pull_request_num_elements_min": 0, "globalq_data_pull_request_num_elements_max": 0,
      00:   "globalq_data_pull_reply_num_elements": 0, "globalq_data_pull_reply_num_elements_count": 0, "globalq_data_pull_reply_num_elements_mean": 0, "globalq_data_pull_reply_num_elements_stddev": 0, "globalq_data_pull_reply_num_elements_min": 0, "globalq_data_pull_reply_num_elements_max": 0,
      00:   "query_runtime": 24.912,
      00:   "scan_runtime": 7.98493,
      00:   "in_memory_runtime": 16.8997,
      00:   "init_runtime": 0.0267438,
      00:   "join_coarse_result_count": 0,
      00:   "emit_count": 4,
      00:
      00: }STATS

      00: STATS{
        00:   "app_1_gce_incomplete": 0,
        00:   "app_2_gce_incomplete": 0,
        00:   "globalq_data_pull_reply_messages": 0,
        00:   "globalq_data_pull_reply_total_bytes": 0,
        00:   "globalq_data_pull_request_num_elements": 0, "globalq_data_pull_request_num_elements_count": 0, "globalq_data_pull_request_num_elements_mean": 0, "globalq_data_pull_request_num_elements_stddev": 0, "globalq_data_pull_request_num_elements_min": 0, "globalq_data_pull_request_num_elements_max": 0,
        00:   "globalq_data_pull_reply_num_elements": 0, "globalq_data_pull_reply_num_elements_count": 0, "globalq_data_pull_reply_num_elements_mean": 0, "globalq_data_pull_reply_num_elements_stddev": 0, "globalq_data_pull_reply_num_elements_min": 0, "globalq_data_pull_reply_num_elements_max": 0,
        00:   "query_runtime": 24.912,
        00:   "scan_runtime": 7.98493,
        00:   "in_memory_runtime": 16.8997,
        00:   "init_runtime": 0.0267438,
        00:   "join_coarse_result_count": 0,
        00:   "emit_count": 4,
        00:
        00: }STATS
        """)

dbfile = 'newtest.db'
db = dataset.connect('sqlite:///{0}'.format(dbfile))

table = db['newtable']

# bulk insert
db.begin()

for x in i:
  # find the next experimental result
  found = x.group(0)

  # remove STATS tags
  notags = re.sub(statspat, '', found)

  # remove mpi logging node ids
  noids = re.sub(frontpat, '', notags)

  # json doesn't allow trailing comma
  notrailing = re.sub(lastcomma, '}', noids)

  asdict = json.loads(notrailing)
  table.insert(asdict)

db.commit()
