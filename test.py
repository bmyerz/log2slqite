import sqliteprocessor
from grappa_parser import GrappaLogParser
import log2sqlite

logstr = """
    00: PARAMS{
      00:   "nnode": 8,
      00:   "ppn": 12,
      00:
      00: }PARAMS
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

    00: PARAMS{
      00:   "nnode": 4,
      00:   "ppn": 6,
      00:
      00: }PARAMS

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
        """

log2sqlite.run(logstr, GrappaLogParser(),
        sqliteprocessor.SQLiteProcessor('test/test.db', 'experiments'))

