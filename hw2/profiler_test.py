
from profiler import Profiler
from myclass import Myclass

import time


# Define a couple of functions to be profiled

@Profiler.profile
def inner():
    time.sleep(0.03)

@Profiler.profile
def myfunc(x,y):
    time.sleep(0.02)
    for i in range(5):
        inner()
    return x + y


# Run some code
mc = Myclass()

for i in range(10):
    myfunc(i,i)
    print(mc.my_method(i,i))



# Print the profiling report
Profiler.report()




