#!/usr/bin/env python3

import timeit
import sys
from functools import reduce

class SquaresSum:
    def loop_test(last_number: int):
        sum = 0
        for num in range(1, last_number + 1):
            sum += num**2
        return sum

    def reduce_test(last_number: int):
        return reduce(lambda x: prev + next**2, range(1, last_number + 1))         
    
def main(test: str, itr: str,  nbr: str):

    results = {
        'loop': SquaresSum.loop_test,
        'reduce': SquaresSum.reduce_test,
    }

    try:
        itr = int(itr)
        nbr = int(nbr)
        if test not in results.keys():
            raise Exception()
    except:
        print("Invalid arguments.")
        return
    
    print(timeit.timeit(lambda: results[test](nbr), number=itr))

if __name__ == '__main__':
    if len(sys.argv) == 4:
        main(sys.argv[1], sys.argv[2], sys.argv[3])