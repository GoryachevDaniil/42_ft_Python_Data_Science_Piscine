#!/usr/bin/env python3

import timeit

class Gmails:
        emails = ['john@gmail.com', 'james@gmail.com', \
                    'alice@yahoo.com', 'anna@live.com', \
                    'philipp@gmail.com'] * 5

        domain = '@gmail.com'

        def loop_test():
            result = []
            for email in Gmails.emails:
                if email.find(Gmails.domain) != -1:
                    result.append(email) 
            return result 

        def list_comprehension_test():
            return [email for email in Gmails.emails if email.find(Gmails.domain) != -1]

        def map_test():
            return list(map(lambda x: x.find(Gmails.domain) != -1, Gmails.emails))

def main():
    ITER_NBR = 90000000

    time_results = {
        'loop_time': timeit.timeit(Gmails.loop_test, number=ITER_NBR),
        'list_comprehension_time': timeit.timeit(Gmails.list_comprehension_test, number=ITER_NBR),
        'map_time': timeit.timeit(Gmails.map_test, number=ITER_NBR)
    }

    best_result = min(time_results.items(), key=lambda x: x[1])
    print(f'it is better to use a {best_result[0]}')

    result = ""
    for elem in sorted(time_results.values()):
        result += f'{elem} vs '
    print(result[:-4])



if __name__ == '__main__':
    main()