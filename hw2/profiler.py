"""
profiler.py
A profiler class that demonstrates the use of decorators to support code profiling
DS3500: Advanced Programming with Data (Prof. Rachlin)

Using class variables instead of instance variables!

"""
from collections import defaultdict
import time


class Profiler:
    """ A code profiling class.  Keeps track of function calls and running time. """
    calls = defaultdict(int)  # default = 0
    time = defaultdict(float)  # default = 0.0

    def __init__(self):
        """ Constructor """
        pass

    @staticmethod
    def add(name, sec):
        """ Add 1 call and <sec> time to named function tracking """
        Profiler.calls[name] += 1
        Profiler.time[name] += sec

    @staticmethod
    def profile(f):
        """ The profiling decorator """
        def wrapper(*args, **kwargs):
            fname = str(f).split()[1]
            start = time.time_ns()
            val = f(*args, **kwargs)
            sec = (time.time_ns() - start) / 10**9
            Profiler.add(fname, sec)
            return val
        return wrapper

    @staticmethod
    def report():
        """ Summarize # calls, total runtime, and time/call for each function """
        print("Function              Calls     TotSec   Sec/Call")
        for name, num in Profiler.calls.items():
            sec = Profiler.time[name]
            print(f'{name:20s} {num:6d} {sec:10.6f} {sec / num:10.6f}')



