import sys
import os

class Resultearch:
    def __init__(self, path):
        self.path = path

    def file_reader(self):
        header_flag = True
        data = self.check_file(header_flag)

        return data

    def check_file(self, header_flag):
        if not os.access(self.path, os.R_OK):
            raise ValueError("File unread.")
        
        with open(self.path, "r") as f:
            lines = [line.rstrip() for line in f]
        
        if (len(lines) < 1):
            raise ValueError("Size off!")
        
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
        
        result = []
        
        for line in new_lines:
            string_pull = line.split(',')
            numbers = []
            for number in string_pull:
                numbers.append(int(number))
            result.append(list(numbers))
        
        return result

    class Calculations:
        def counts(self, data):
            heads = 0
            tails = 0
            
            for pair in data:
                heads += pair[0]
                tails += pair[1]
            
            return heads, tails

        def fractions(self, heads, tails):
            first = heads * 100 / (heads + tails)
            second = tails * 100 / (heads + tails)
            
            return first, second

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