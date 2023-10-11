from time import perf_counter as pc
from time import sleep as pause

import multiprocessing as mp

### Test utan parallellprogrammering ###

def runner():
    print('Performing a costly function')
    pause(1)
    print('Function complete')

""" if __name__ == "__main__":
    start = pc()
    for i in range(10):
        runner()
    end = pc()
    print(f'Process took {round(end-start, 2)} seconds.') """

### Test med parallellprogrammering ###

if __name__ == "__main__":
    start = pc()
    p1 = mp.Process(target=runner)
    p2 = mp.Process(target=runner)
    p1.start()
    p2.start()
    end = pc()
    print(f'Process took {round(end-start, 2)} seconds.')