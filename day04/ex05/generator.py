#!/usr/bin/env python3

import sys
import resource

def read_lines(file: str):
    with open(file, 'r', encoding='utf-8') as file:
        line = 'dummy'
        while line:
            line = file.readline()
            yield line

def main(file: str):
    for line in read_lines(file):
        pass

    usage = resource.getrusage(resource.RUSAGE_SELF)
    print(f'Peak Memory Usage = {(usage.ru_maxrss / (1024**3)):.3f} GB')
    print(f'User Mode Time + System Mode Time = {(usage.ru_utime + usage.ru_stime):.2f}s')

if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])