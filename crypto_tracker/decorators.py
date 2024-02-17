# import psutil
from memory_profiler import profile

@profile
def func():
    # print(psutil.cpu_count(logical=False))
    print('')

func()
