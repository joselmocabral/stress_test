import argparse
from datetime import datetime, timedelta
import random
import threading
import time
import sys

class StressTest:
    THROUGHPUT_UPPER = 100000
    LATENCY_UPPER = 20000
    
    def __init__(self, stress_duration):
        self._duration = stress_duration
        self._time = datetime.now()
        self._throughput = self.random_boundarie(self.THROUGHPUT_UPPER)
        self._latency = self.random_boundarie(self.LATENCY_UPPER)
        self._thread = threading.Thread(target=self.start_logging)
        self._thread.start()

    @staticmethod
    def random_boundarie(upper_limit):
        '''
        Returns a random number based on an upper limit
        '''
        return random.randint(0, upper_limit)

    def new_second(self):
        self.output_results()
        self._time += timedelta(seconds=1)
        self._duration -=1
        self._throughput = self.random_boundarie(self.THROUGHPUT_UPPER)
        self._latency = self.random_boundarie(self.LATENCY_UPPER)

    def output_results(self):
        print(f"thread {self._thread.ident} | seconds {self._time} | throughput {self._throughput} | latency {self._latency}")

    def start_logging(self):
        while self._duration:
            self.new_second()
            time.sleep(1)

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--stress_duration', help='Please provide duration of test')
    args=parser.parse_args()

    stress_duration = int(args.stress_duration)

    thread = StressTest(stress_duration = stress_duration)
