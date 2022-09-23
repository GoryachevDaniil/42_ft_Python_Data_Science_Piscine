# #!/usr/bin/env python3

import timeit

class Gmails:
        emails = ['john@gmail.com', 'james@gmail.com', \
                    'alice@yahoo.com', 'anna@live.com', \
                    'philipp@gmail.com'] * 5

        domain = '@gmail.com'

        def loop_test():
            lst = []
            for email in Gmails.emails:
                if email.find(Gmails.domain) != -1:
                    lst.append(email) 
            return lst 

        def list_comprehension_test():
            return [email for email in Gmails.emails if email.find(Gmails.domain) != -1]

def main():
    ITER_NBR = 90000000

    loop_time = timeit.timeit(Gmails.loop_test, number=ITER_NBR)
    list_comprehension_time = timeit.timeit(Gmails.list_comprehension_test, number=ITER_NBR)

    print('it is better to use a list comprehension') if list_comprehension_time < loop_time \
            else print('it is better to use a loop')

    print(f'{min(loop_time, list_comprehension_time)} vs {max(loop_time, list_comprehension_time)}')

if __name__ == '__main__':
    main()