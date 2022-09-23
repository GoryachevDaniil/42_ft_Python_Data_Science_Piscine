import sys
from random import randint

class Research:
    def __init__(self, path):
        self.path = path

    def file_reader(self):
        header_flag = True
        data = self.check_file(header_flag)

        return data

    def check_file(self, header_flag):
        with open(self.path, "r") as f:
            lines = [line.rstrip() for line in f]
        
        if (len(lines) < 1):
            raise ValueError("Size off.")
        
        if lines[0] == "0,1" or lines[0] == "1,0":
            header_flag = False
        
        if header_flag and len(lines[0].split(',')) != 2:
            raise ValueError("Header invalid.")
        
        new_lines = []
        
        if header_flag:
            new_lines = lines[1:]
        else:
            new_lines = lines
        
        for line in new_lines:
            if line != "0,1" and line != "1,0":
                raise ValueError("Data invalid.")
        
        res = []
        
        for line in new_lines:
            string_pull = line.split(',')
            numbers = []
            for number in string_pull:
                numbers.append(int(number))
            res.append(list(numbers))
        
        return res

    class Calculations:
        def __init__(self, data):
            self.data = data

        def counts(self):
            heads = 0
            tails = 0
            for pair in self.data:
                heads += pair[0]
                tails += pair[1]
            
            return heads, tails

        def fractions(self, heads, tails):
            first = heads * 100 / (heads + tails)
            second = tails * 100 / (heads + tails)
            
            return first, second

    class Analytics(Calculations):
        def predict_random(self, num):
            res = []
            
            for i in range(num):
                first = randint(0, 1)
                second = 0 if first else 1
                res.append([first, second])
            
            return res

        def predict_last(self, res):
            
            return res[-1]

def analytic_test():
    inherited = researcher.Analytics(researcher.file_reader())
    rand_nums = inherited.predict_random(3)
    print(rand_nums)
    print(inherited.predict_last(rand_nums))

def calc_test(researcher):
    calc_test(researcher)
    input_value = researcher.Calculations()
    calc = input_value.counts(researcher.file_reader())
    print(calc[0], calc[1])
    fr = input_value.fractions(calc[0], calc[1])
    print(frac[0], frac[1])

def main():
    researcher = Research(sys.argv[1])
    print(researcher.file_reader())
    calc_test(researcher)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        raise ValueError("No file")
