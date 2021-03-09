import argparse
import random
import re
import subprocess
import tempfile


from stress import StressTest

class Result:

    def __init__(self, thread_id, timestamp, throughput, latency):
        self._thread_id = thread_id
        self._timestamp = timestamp
        self._throughput = throughput
        self._latency = latency

    @property
    def throughput(self):
        return self._throughput

    @property
    def latency(self):
        return self._latency

    @property
    def thread_id(self):
        return self._thread_id

    @property
    def timestamp(self):
        return self._timestamp

class Analysis:

    def __init__(self, n_threads):
        self._results = []
        self._durations = list(range(5, n_threads*2)) if n_threads > 15 else list(range(5, 31))

    def add_result(self, thread_id, timestamp, throughput, latency):
        new_result = Result(thread_id, timestamp, throughput, latency)
        self._results.append(new_result)

    def extract_data(self, s):
        values = s.split(' | ')
        thread_id = str(values[0].split(' ')[-1])
        timestamp = str(values[1].split(' ')[-1])
        throughput = int(values[2].split(' ')[-1])
        latency = int(values[3].split(' ')[-1])
        self.add_result(thread_id, timestamp, throughput, latency)

    def overall_stats(self):
        print("Processes Statistics Report:")
        processes = set([p.thread_id for p in self._results])
        id_timestamp = [(p.thread_id, p.timestamp) for p in self._results]
        for p in processes:
            print(f"thread id: {p}")
            timestamps = [r[1] for r in id_timestamp if r[0] == p]
            print(f"started at: {timestamps[0]}")
            print(f"ended at: {timestamps[-1]}")
            print(f"duration: {len(timestamps)-1}")
        
    def throughput_stats(self):
        print("Throughput Statistics Report:")
        throughput_results = sorted([result.throughput for result in self._results])
        position_95th = int(0.95*len(throughput_results))
        position_95th = position_95th - 1 if position_95th > 0 else 0
        print(f"avg_value: {sum(throughput_results)/len(throughput_results)} operations/s")
        print(f"min_value: {min(throughput_results)} operations/s")
        print(f"max_value: {max(throughput_results)} operations/s")
        print(f"95th_percentile: {throughput_results[position_95th]} operations/s")

    def latency_stats(self):
        print("Latency Statistics Report:")
        latency_results = sorted([result.latency for result in self._results])
        position_95th = int(0.95*len(latency_results))
        position_95th = position_95th - 1 if position_95th > 0 else 0
        print(f"avg_value: {sum(latency_results)/len(latency_results)} operations/s")
        print(f"min_value: {min(latency_results)} operations/s")
        print(f"max_value: {max(latency_results)} operations/s")
        print(f"95th_percentile: {latency_results[position_95th]} operations/s")

    def duration_generator(self):
        return self._durations.pop(random.randint(0,len(self._durations)-1))

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--n_threads', help='Please provide amount of threads to be ran')
    args=parser.parse_args()
    n_threads = int(args.n_threads)
    analysis_summary = Analysis(n_threads)
    cmds_list = [["python", "./stress.py", "--stress_duration", str(analysis_summary.duration_generator())] for i in range(n_threads)]
    procs_list = [subprocess.Popen(cmd, stdout=subprocess.PIPE) for cmd in cmds_list]
    for proc in procs_list:
        proc.wait()
    for proc in procs_list:
        for line in proc.stdout:
            analysis_summary.extract_data(str(line.strip())[:-1])
    print(f"{n_threads} processes were ran during this stress test")
    analysis_summary.overall_stats()
    analysis_summary.throughput_stats()
    analysis_summary.latency_stats()
