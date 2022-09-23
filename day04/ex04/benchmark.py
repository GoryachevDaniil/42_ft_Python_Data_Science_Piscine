#!/usr/bin/env python3

import timeit
from random import randint
from collections import Counter

class CounterRand:
    min_value = 0
    max_value = 100
    
    def __init__(self, list_size: int) -> None:
        self.random_list = [randint(self.min_value, self.max_value) for _ in range(list_size)]
        self.cached_counts_loop = None
        self.cached_counts_counter = None

    def loop_test(self):
        counts = {}
        for value in self.random_list:
            if value in counts.keys(): 
                counts[value] += 1 
            else: 
                counts[value] = 1
        self.cached_counts_loop = counts
        return counts

    def counter_test(self):
        self.cached_counts_counter = Counter(self.random_list)
        
        return dict(self.cached_counts_counter)

    def top_10_loop_test(self):
        if self.cached_counts_loop is None:
            self.get_counts_with_loop()
            
        return dict(sorted(self.cached_counts_loop.items(), 
                      key=lambda item: item[1], reverse=True)[:10])

    def top_10_counter_test(self):
        if self.cached_counts_counter is None:
            self.get_counts_with_loop()
            
        return self.cached_counts_counter.most_common(10)

def main():
    ITER_NBR = 10000

    tester = CounterRand(1000)

    test_functions =  {
        'my function': tester.loop_test,
        'Counter': tester.counter_test,
        'my top': tester.top_10_loop_test,
        "Counter's top": tester.top_10_loop_test
    }

    time_results = map(lambda func: (func[0], timeit.timeit(func[1], \
                        number=ITER_NBR)), test_functions.items())
    
    for func_name, time in time_results:
        print(f'{func_name}: {time}')

if __name__ == '__main__':
    main()