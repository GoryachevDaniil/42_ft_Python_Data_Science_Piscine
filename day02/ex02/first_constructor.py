import sys
import os

class Research:
    def __init__(self, path):
        self.path = path

    def file_reader(self):
        data = self.check_file()
        return data

    def check_file(self):
        if not os.access(self.path, os.R_OK):
            raise ValueError("File unread.")
        
        with open(self.path, "r") as f:
            lines = [line.rstrip() for line in f]
        
        if (len(lines) < 2):
            raise ValueError("Size off!")
        
        if lines[0] == "0,1" or lines[0] == "1,0" 
            raise ValueError("Header invalid.")
        
        if len(lines[0].split(',')) != 2:
            raise ValueError("Header invalid.")
        
        for line in lines[1:]:
            if line != "0,1" and line != "1,0":
                raise ValueError("Data invalid.")
        
        return "\n".join(lines)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        r = Research(sys.argv[1])
        print(r.file_reader())
    else:
        raise ValueError("No input file")