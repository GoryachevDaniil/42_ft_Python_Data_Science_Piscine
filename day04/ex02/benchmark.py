#!/usr/bin/env python3

import timeit
import sys

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

        def filter_test() -> list:
            return list(filter(lambda x: x.find(Gmails.domain) != -1, Gmails.emails))

def main(test: str, itr: str):

    results = {
        'loop_test': Gmails.loop_test,
        'list_comprehension_test': Gmails.list_comprehension_test,
        'map_test': Gmails.map_test,
        'filter_test': Gmails.filter_test
    }

    try:
        itr = int(itr)
        if test not in results.keys():
            raise Exception()
    except:
        print("Invalid arguments.")
        return
    
    print(timeit.timeit(results[test], number=itr))

if __name__ == '__main__':
    if len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])